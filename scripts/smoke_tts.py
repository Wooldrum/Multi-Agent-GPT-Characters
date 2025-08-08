#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import requests


def main():
    load_dotenv()
    base_url = os.getenv('COQUI_TTS_URL', 'http://127.0.0.1:5002').rstrip('/')
    language_idx = os.getenv('LANGUAGE_IDX', 'en')
    speaker_wav = os.getenv('SPEAKER_WAV', '').strip()

    url = f"{base_url}/api/tts"
    data = {
        'text': 'This is a test of the local Coqui XTTS server.',
        'model_name': 'tts_models/multilingual/multi-dataset/xtts_v2',
        'language_idx': language_idx,
    }
    files = None
    opened = None
    try:
        if speaker_wav and os.path.isfile(speaker_wav):
            opened = open(speaker_wav, 'rb')
            files = {'speaker_wav': opened}
        resp = requests.post(url, data=data, files=files, timeout=60)
        resp.raise_for_status()
    finally:
        if opened:
            opened.close()

    out_dir = os.path.join(os.path.abspath(os.curdir), 'static', os.getenv('AUDIO_OUT_DIR', 'audio_out'))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'test.wav')
    with open(out_path, 'wb') as f:
        f.write(resp.content)
    print(f"Wrote {out_path}")


if __name__ == '__main__':
    main()

