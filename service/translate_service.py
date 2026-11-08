import json, requests, os

MODEL = "gemma4:12b"
OLLAMA_URL = "https://my.domain.net/ollama"

class OllamaError(Exception):
    pass

def translate(text, source_lang, dest_lang, words):
    try:
        r = requests.post(f"{OLLAMA_URL}/api/chat",
                          json= {"model": MODEL,
                                 "messages": [{"role": "user", "content": f"Translate from {source_lang} to {dest_lang}. Output only translation \n {text}"}],
                                                "stream": False,
                                                "think": False,
                                                "options": {"temperature": 0}}, timeout=(5, 180),
                          )
    except requests.RequestException as exc:
        raise OllamaError(str(exc)) from exc
    if r.status_code != 200:
        raise OllamaError(r.text[:200])
    return r.json()["message"]["content"].strip()
