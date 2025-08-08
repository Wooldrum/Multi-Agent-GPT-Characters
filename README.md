# Multi Agent GPT Characters (Local LLM + TTS)

This version runs all AI components locally:
- Ollama (OpenAI-compatible endpoint) for chat
- Coqui XTTS-v2 via `tts-server` for text-to-speech

The Flask UI runs at `127.0.0.1:5151`.

## Quickstart (Local Only)

1) Install Python and dependencies
   - `pip install -r requirements.txt`

2) Install and run Ollama
   - Install: https://ollama.com/download
   - Run: `ollama serve`
   - Pull a model: `ollama pull gpt-oss-120b` (or another chat model)

3) Run Coqui XTTS server
   - Install: `pip install TTS`
   - Start: `tts-server --model_name tts_models/multilingual/multi-dataset/xtts_v2 --host 127.0.0.1 --port 5002`

4) Configure environment
   - `cp .env.example .env`
   - Optionally set `SPEAKER_WAV` to a local reference audio file

5) Start the app
   - `python multi_agent_gpt.py`

## Smoke Tests
- `python scripts/smoke_ollama.py` (checks chat path)
- `python scripts/smoke_tts.py` (writes `./audio_out/test.wav`)

## OBS Notes
OBS integration remains optional. Ensure OBS WebSocket is enabled and configured per `obs_websockets.py`/`websockets_auth.py`.

## Troubleshooting
- Ollama: ensure `ollama serve` is running and the model name in `.env` exists (`ollama list`). Confirm `OPENAI_BASE_URL=http://localhost:11434/v1`.
- Coqui: 500 errors usually indicate model not loaded or invalid `SPEAKER_WAV`. Restart `tts-server` and verify the path.

## Notes
- Whisper transcription remains local via HuggingFace Whisper Large V3. Install CUDA-enabled PyTorch for best performance.
