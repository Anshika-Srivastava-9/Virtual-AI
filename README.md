# Virtual AI Desktop Assistant

A simple Python desktop AI assistant with GUI. It performs basic tasks via natural-language commands and supports optional voice input and online summarization.

Features

- Web search (opens your browser)
- Summarize user input (local summarizer)
- Optional online summarization via OpenAI when `OPENAI_API_KEY` is set
- Read content aloud (text-to-speech with `pyttsx3`)
- Basic calculations (safe AST-based evaluator)
- Voice input (microphone) via `SpeechRecognition` (optional)
- Menu, keyboard shortcuts, and a helper `build.sh` for packaging with `pyinstaller`

Requirements

- Python 3.8+ recommended
- See `requirements.txt` for Python packages. Core runtime packages:
  - `pyttsx3` (text-to-speech)
  - `SpeechRecognition` (optional, voice input)
  - `openai` (optional, online summarization)
  - `pyinstaller` (optional, packaging)

Install dependencies (recommended in a virtualenv):

```bash
pip install -r requirements.txt
```

Notes:

- Microphone input needs a working microphone and a backend. On many Linux systems you may need to install system packages and `pyaudio` or use `sounddevice`.
- To enable online summarization, export `OPENAI_API_KEY` in your environment. The app will fall back to a local summarizer when no key is present.

Usage

1. Clone this repository:

```bash
git clone https://github.com/Anshika-Srivastava-9/virtual-ai.git
cd virtual-ai
```

2. Run the assistant:

```bash
python virtual_ai_gui.py
```

3. Commands (typed into the app):

- `search cats` → Opens browser and searches for “cats”.
- `summarize` → Prompts for text to summarize (local summarizer).
- `summarize online` → If `OPENAI_API_KEY` is set, uses OpenAI to summarize.
- `read aloud` → Prompts for text to read aloud.
- `calculate 7*9+12` → Calculates and displays the result.
- `open browser` → Opens Google homepage.
- `exit` → Closes the app.

Voice input

- Press the `Listen` button or press `Ctrl+L` to record voice and convert to text (requires `SpeechRecognition` and a microphone).

Packaging

- Build a single-file executable (optional):

```bash
./build.sh
```

Extending

To add new features (weather, reminders, etc.), edit `virtual_ai_gui.py` and add more commands inside `handle_command()` or add tools in the menu.

---

**Author:** Anshika-Srivastava-9  
**License:** MIT
