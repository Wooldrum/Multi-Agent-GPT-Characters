import os
import time
import uuid
from typing import Optional

import requests
from dotenv import load_dotenv


class CoquiTTSManager:
    """
    Minimal TTS client for a local Coqui XTTS server.

    Exposes a text_to_audio method compatible with the existing ElevenLabsManager
    signature. Always returns a wav file path saved under ./tts_cache.
    """

    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("COQUI_TTS_URL", "http://127.0.0.1:5002")
        self.language_idx = os.getenv("LANGUAGE_IDX", "en")
        self.speaker_wav = os.getenv("SPEAKER_WAV", "").strip()

        out_dir = os.getenv("AUDIO_OUT_DIR", "audio_out")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(base_dir, "static", out_dir)
        os.makedirs(self.output_dir, exist_ok=True)

    def text_to_audio(self, input_text: str, voice: str = "", save_as_wave: bool = True,
                      subdirectory: str = "", model_id: str = "xtts_v2") -> str:
        """
        Convert text to speech via Coqui server and return saved wav file path.

        Parameters mirror ElevenLabsManager for drop-in compatibility.
        - input_text: text to synthesize
        - voice: unused; kept for API compatibility (use TTS_SPEAKER env instead)
        - save_as_wave: ignored; Coqui returns wav and we persist wav
        - subdirectory: optional subfolder under ./tts_cache for the output
        - model_id: unused; for compatibility
        """

        url = f"{self.base_url.rstrip('/')}/api/tts"
        files = None

        data = {
            "text": input_text,
            "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
            "language_idx": self.language_idx,
        }

        # Optional voice cloning file
        opened_file: Optional[object] = None
        try:
            if self.speaker_wav:
                clone_path = os.path.expanduser(self.speaker_wav)
                if os.path.isfile(clone_path):
                    opened_file = open(clone_path, "rb")
                    files = {"speaker_wav": opened_file}

            resp = requests.post(url, data=data, files=files, timeout=60)
            resp.raise_for_status()

            # Build output path
            # Determine file name as ./audio_out/agent_<n>_<timestamp>.wav
            agent_tag = "agent_0"
            if model_id and isinstance(model_id, str) and model_id.startswith("agent_"):
                agent_tag = model_id
            timestamp = int(time.time())
            filename = f"{agent_tag}_{timestamp}.wav"
            out_path = os.path.join(self.output_dir, filename)

            with open(out_path, "wb") as f:
                f.write(resp.content)

            return out_path
        finally:
            if opened_file:
                try:
                    opened_file.close()
                except Exception:
                    pass
