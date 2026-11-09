import json, requests, os

from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import Translation, Chunk, TranslationChunk

MODEL = "gemma4:12b"
OLLAMA_URL = "https://my.domain.net/ollama"

class OllamaError(Exception):
    pass

def translate(text, source_lang, dest_lang):
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat",
                          json= {"model": MODEL,
                                 "messages": [{"role": "user", "content": f"Translate from {source_lang} to {dest_lang} and give word by word breakdown  "
                                                                        + """ 
                                                                          Return exactly two kinds of lines, nothing else:
                                                                            T: <full translation on one line>
                                                                            W: <chunk> | <short meaning>
                                                                            One W: line per chunk, in order. No markdown, no extra text.
                                                                          """
                                                                          f"\n {text}"}],
                                                "stream": False,
                                                "think": False,
                                                "options": {"temperature": 0}}, timeout=(5, 180),
                          )
    except requests.RequestException as exc:
        raise OllamaError(str(exc)) from exc
    if r.status_code != 200:
        raise OllamaError(r.text[:200])
    return parse(r.json()["message"]["content"].strip())

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


def translate_and_store(text, source_lang, dest_lang, db: Session):
    response = translate(text, source_lang, dest_lang)
    tr = Translation(
        query=text,
        translation=response["translation"],
        source_lang=source_lang,
        dest_lang=dest_lang
    )
    db.add(tr)
    db.flush()
    response["id"] = tr.id
    for seq, word in enumerate(response["words"], start=1):
        chunk = word["chunk"].strip()
        if not chunk:
            continue
        stmt = insert(Chunk).values(text=chunk)
        stmt = stmt.on_conflict_do_update(
            index_elements=[Chunk.text],
            set_={"times_used": Chunk.times_used + 1, "last_used": func.now()}
        ).returning(Chunk.id)
        chunk_id = db.execute(stmt).scalar_one()
        word["id"] = chunk_id
        db.add(TranslationChunk(
            translation_id=tr.id,
            chunk_id=chunk_id,
            stored_meaning=word["meaning"],
            sequence_number=seq
        ))
    return response
