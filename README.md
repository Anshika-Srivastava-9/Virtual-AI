# Virtual AI Desktop Assistant

A simple Python desktop AI assistant with GUI.  
It can perform basic tasks via natural language commands:
- Web search (opens your browser)
- Summarize user input
- Read content aloud (text-to-speech)
- Basic calculations
- GUI entry/output

## Features

- **Type commands** into the GUI and get instant results.
- **Voice responses** via text-to-speech (pyttsx3).
- Easily extensible for more AI tasks!

## Requirements

- Python 3.8+ recommended
- `pyttsx3` for text-to-speech

Install dependencies:
```bash
pip install pyttsx3
```
(Tkinter is included with most Python installations.)

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/Anshika-Srivastava-9/virtual-ai.git
    cd virtual-ai
    ```

2. Run the assistant:

    ```bash
    python virtual_ai_gui.py
    ```

3. In the app window, you can type any of these commands:

    - `search cats`  
      → Opens browser and searches for “cats”.

    - `summarize`  
      → Prompts for text to summarize.

    - `read aloud`  
      → Prompts for text to read aloud.

    - `calculate 7*9+12`  
      → Calculates and displays the result.

    - `open browser`  
      → Opens Google homepage.

    - `exit`  
      → Closes the app.

## Extending

To add new features (weather, reminders, etc.), edit `virtual_ai_gui.py` and add more commands to `handle_command()`.

---

**Author:** Anshika-Srivastava-9  
**License:** MIT (recommend adding a LICENSE file for open source projects)
