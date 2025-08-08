import os
import sys
import requests
from dotenv import load_dotenv


def check_ollama():
    base_url = os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:11434/v1").rstrip("/")
    model = os.getenv("OPENAI_MODEL", "llama3.1:8b-instruct")
    try:
        resp = requests.get(f"{base_url}/models", timeout=5)
        resp.raise_for_status()
        models = [m.get("id") for m in resp.json().get("data", [])]
        if model not in models:
            print(f"[WARN] Model '{model}' not found at {base_url}")
        else:
            print("[OK] Ollama reachable")
        return True
    except Exception as e:
        print(f"[ERROR] Ollama check failed: {e}")
        return False


def check_coqui():
    tts_url = os.getenv("COQUI_TTS_URL", "http://127.0.0.1:5002").rstrip("/")
    speaker = os.getenv("SPEAKER_WAV", "").strip()
    data = {"text": "Hello from preflight"}
    if speaker:
        data["speaker_wav"] = speaker
    try:
        resp = requests.post(f"{tts_url}/api/tts", json=data, timeout=10)
        resp.raise_for_status()
        if not resp.content.startswith(b"RIFF"):
            print("[ERROR] Coqui TTS did not return WAV data")
            return False
        print("[OK] Coqui TTS reachable")
        return True
    except Exception as e:
        print(f"[ERROR] Coqui TTS check failed: {e}")
        return False


def run_preflight():
    load_dotenv()
    ok1 = check_ollama()
    ok2 = check_coqui()
    if ok1 and ok2:
        print("[OK] All services healthy.")
        return True
    return False


if __name__ == "__main__":
    if not run_preflight():
        sys.exit(1)

