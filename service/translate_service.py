import json, requests, os

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
