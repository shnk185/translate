import json, requests, os

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import Translation, Chunk, TranslationChunk, PresetConfig, Prompt

MODEL = "gemma4:12b"
OLLAMA_URL = "https://my.domain.net/ollama"

class OllamaError(Exception):
    pass

def translate(text, source_lang, dest_lang, prompt_list):
    messages = [{"role": "user", "content": p.text} for p in prompt_list]
    messages.append({"role": "user", "content": f"Translate from {source_lang} to {dest_lang} and give word by word breakdown  "
                                                                        + """ 
                                                                          Return exactly two kinds of lines, nothing else:
                                                                            T: <full translation on one line>
                                                                            W: <chunk> | <short meaning> (one new line on every single chunk with W: prefix)
                                                                            No markdown, no extra text.
                                                                          """
                                                                          f"\n {text}"})
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat",
                          json= {"model": MODEL, "messages": messages, "stream": False, "think": False,"options":
                              {"temperature": 0}}, timeout=(5, 180),)
    except requests.RequestException as exc:
        raise OllamaError(str(exc)) from exc
    if r.status_code != 200:
        raise OllamaError(r.text[:200])
    raw_response = r.json()["message"]["content"].strip()
    print(raw_response)
    return parse(raw_response)


def get_preset_prompts(db: Session, preset_id: int) -> list[Prompt]:
    return list(db.execute(
        select(Prompt)
        .join(PresetConfig, PresetConfig.prompt_id == Prompt.id)
        .where(PresetConfig.preset_id == preset_id)
        .order_by(PresetConfig.id)
    ).scalars())


def parse(text):
    t, words = None, []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        elif line.startswith("T:"):
            t = line[2:].strip()
        elif line.startswith("W:"):
            chunk, _, meaning = line[2:].strip().partition('|')
            words.append({"chunk": chunk.strip(), "meaning": meaning.strip()})
    return {"translation": t, "words": words}


def translate_and_store(text, source_lang, dest_lang, preset_id, db: Session):
    prompt_list = get_preset_prompts(db, preset_id)
    response = translate(text, source_lang, dest_lang, prompt_list)
    tr = Translation(query=text, translation=response["translation"], source_lang=source_lang, dest_lang=dest_lang)
    db.add(tr)
    db.flush()
    response["id"] = tr.id
    for seq, word in enumerate(response["words"], start=1):
        chunk = word["chunk"].strip()
        if not chunk:
            continue

        stmt = insert(Chunk).values(text=chunk)
        stmt = stmt.on_conflict_do_update(index_elements=[Chunk.text],
            set_={"times_used": Chunk.times_used + 1, "last_used": func.now()}
        ).returning(Chunk.id, Chunk.known)
        chunk_id, known = db.execute(stmt).one()
        word["id"] = chunk_id
        word["known"] = known
        db.add(TranslationChunk(translation_id=tr.id, chunk_id=chunk_id, stored_meaning=word["meaning"],
                                sequence_number=seq))
    return response
