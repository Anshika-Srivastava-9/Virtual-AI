# Virtual AI — Quick Start

Minimal quick-start instructions to run the Virtual AI desktop assistant locally.

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app (opens a GUI window):

```bash
python virtual_ai_gui.py
```

Notes:
- If you're on a headless server (no GUI/display), the app cannot show a window. For testing in CI or headless environments, you can run a smoke import test:

```bash
python -c "import virtual_ai_gui; print('import OK')"
```

- To enable online summarization, export `OPENAI_API_KEY` in your environment.
- Voice input requires a microphone and appropriate backend (e.g., `pyaudio`).
