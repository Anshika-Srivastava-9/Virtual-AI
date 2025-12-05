import ast
import re
import webbrowser
from collections import Counter
from urllib.parse import quote_plus
import os
import threading
import logging
import tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox

try:
    import pyttsx3
except Exception:
    pyttsx3 = None

try:
    import speech_recognition as sr
except Exception:
    sr = None

try:
    import openai
except Exception:
    openai = None

logging.basicConfig(level=logging.INFO)


def summarize_text_local(text, max_sentences=3):
    if not text:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    if len(sentences) <= max_sentences:
        return text.strip()

    words = re.findall(r"\w+", text.lower())
    stop_words = set([
        "the", "and", "is", "in", "it", "of", "to", "a", "that", "this",
        "for", "on", "with", "as", "are", "was", "by", "be",
    ])
    freqs = Counter(w for w in words if w not in stop_words)

    def score_sentence(s):
        return sum(freqs.get(w.lower(), 0) for w in re.findall(r"\w+", s))

    ranked = sorted(sentences, key=score_sentence, reverse=True)
    summary = " ".join(ranked[:max_sentences])
    return summary


def summarize_text_online(text, max_sentences=3):
    api_key = os.environ.get('OPENAI_API_KEY')
    if not openai or not api_key:
        raise RuntimeError('OpenAI not configured')
    openai.api_key = api_key
    prompt = (
        "Summarize the following text in " + str(max_sentences) + " sentences:\n\n" + text
    )
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2,
            max_tokens=400,
        )
        summary = resp['choices'][0]['message']['content'].strip()
        return summary
    except Exception as e:
        logging.exception('OpenAI summarize failed')
        raise


def summarize_text(text, max_sentences=3, prefer_online=False):
    if prefer_online:
        try:
            return summarize_text_online(text, max_sentences)
        except Exception:
            # fall back to local
            logging.info('Falling back to local summarizer')
    return summarize_text_local(text, max_sentences)


class SafeEval(ast.NodeVisitor):
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.FloorDiv,
        ast.USub,
        ast.UAdd,
        ast.Load,
        ast.BitXor,
        ast.LShift,
        ast.RShift,
        ast.BitAnd,
        ast.BitOr,
        ast.MatMult,
        ast.Tuple,
        ast.List,
    )

    def visit(self, node):
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
        return super().visit(node)


def safe_eval(expr):
    expr = expr.strip()
    if not expr:
        raise ValueError("Empty expression")
    if re.search(r'[a-zA-Z]', expr):
        raise ValueError("Expression contains invalid characters")

    node = ast.parse(expr, mode='eval')
    for n in ast.walk(node):
        if isinstance(n, ast.Call):
            raise ValueError("Function calls are not allowed")

    code = compile(node, '<string>', 'eval')
    return eval(code, {'__builtins__': {}}, {})


class VirtualAIGUI:
    def __init__(self, root):
        self.root = root
        root.title('Virtual AI Desktop Assistant')

        # Menu
        menubar = tk.Menu(root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Exit', command=root.quit)
        menubar.add_cascade(label='File', menu=file_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label='Summarize (online if available)', command=lambda: self.menu_summarize())
        menubar.add_cascade(label='Tools', menu=tools_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label='About', command=self.show_about)
        menubar.add_cascade(label='Help', menu=help_menu)
        root.config(menu=menubar)

        # Entry and buttons
        self.entry = tk.Entry(root, width=60)
        self.entry.grid(row=0, column=0, padx=8, pady=8, sticky='we')
        self.entry.bind('<Return>', lambda e: self.on_send())
        self.entry.bind('<Control-Return>', lambda e: self.on_send())

        self.send_btn = tk.Button(root, text='Send', command=self.on_send)
        self.send_btn.grid(row=0, column=1, padx=8, pady=8)

        self.listen_btn = tk.Button(root, text='Listen (Ctrl+L)', command=self.listen_and_handle)
        self.listen_btn.grid(row=0, column=2, padx=8, pady=8)
        root.bind('<Control-l>', lambda e: self.listen_and_handle())

        self.output = scrolledtext.ScrolledText(root, wrap='word', height=16, width=88)
        self.output.grid(row=1, column=0, columnspan=3, padx=8, pady=(0,8))
        self.output.configure(state='disabled')

        self.status = tk.Label(root, text='Ready', anchor='w')
        self.status.grid(row=2, column=0, columnspan=3, sticky='we', padx=8, pady=(0,8))

        if pyttsx3:
            try:
                self.engine = pyttsx3.init()
            except Exception:
                self.engine = None
        else:
            self.engine = None

        self.recognizer_available = sr is not None
        if not self.recognizer_available:
            logging.info('SpeechRecognition not available; voice input disabled')

    def show_about(self):
        messagebox.showinfo('About', 'Virtual AI Desktop Assistant\nAuthor: Anshika-Srivastava-9')

    def log(self, text):
        self.output.configure(state='normal')
        self.output.insert('end', text + '\n')
        self.output.see('end')
        self.output.configure(state='disabled')

    def speak(self, text):
        if not self.engine:
            self.log('[TTS not available]')
            return
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            self.log(f'[TTS error] {e}')

    def on_send(self):
        cmd = self.entry.get().strip()
        if not cmd:
            return
        self.entry.delete(0, 'end')
        self.log(f'> {cmd}')
        try:
            self.handle_command(cmd)
        except Exception as e:
            self.log(f'Error: {e}')

    def listen_and_handle(self):
        if not self.recognizer_available:
            self.log('Voice input not available (install SpeechRecognition & microphone backend)')
            return

        def worker():
            r = sr.Recognizer()
            with sr.Microphone() as mic:
                self.status.config(text='Listening...')
                audio = r.listen(mic, timeout=5, phrase_time_limit=10)
                self.status.config(text='Recognizing...')
                try:
                    text = r.recognize_google(audio)
                    self.log(f'[Voice] {text}')
                    self.handle_command(text)
                except Exception as e:
                    self.log(f'Voice recognition error: {e}')
                finally:
                    self.status.config(text='Ready')

        t = threading.Thread(target=worker, daemon=True)
        t.start()

    def menu_summarize(self):
        text = simpledialog.askstring('Summarize (online)', 'Enter text to summarize:')
        if not text:
            return
        try:
            self.log('Summarizing (online preferred)...')
            summary = summarize_text(text, prefer_online=True)
            self.log('Summary:')
            self.log(summary)
        except Exception as e:
            self.log(f'Summarization error: {e}')

    def handle_command(self, cmd):
        low = cmd.lower()
        if low.startswith('search '):
            query = cmd[7:].strip()
            if not query:
                self.log('Please provide a search query.')
                return
            url = f'https://www.google.com/search?q={quote_plus(query)}'
            webbrowser.open(url)
            self.log(f'Opened browser search for: {query}')
            self.status.config(text='Opened browser')

        elif low == 'open browser' or low == 'open google':
            webbrowser.open('https://www.google.com')
            self.log('Opened Google in browser.')
            self.status.config(text='Opened browser')

        elif low.startswith('calculate'):
            expr = cmd[len('calculate'):].strip()
            if not expr:
                self.log('Please provide an expression to calculate.')
                return
            try:
                result = safe_eval(expr)
                self.log(f'{expr} = {result}')
                self.status.config(text='Calculated')
            except Exception as e:
                self.log(f'Calculation error: {e}')

        elif low == 'summarize' or low.startswith('summarize '):
            text = None
            if low == 'summarize':
                text = simpledialog.askstring('Summarize', 'Enter text to summarize:')
            else:
                text = cmd[len('summarize'):].strip()
            if not text:
                self.log('No text provided for summarization.')
                return
            self.log('Summarizing...')
            try:
                summary = summarize_text(text)
                self.log('Summary:')
                self.log(summary)
                self.status.config(text='Summarized')
            except Exception as e:
                self.log(f'Summarization error: {e}')

        elif low == 'read aloud' or low.startswith('read aloud '):
            text = None
            if low == 'read aloud':
                text = simpledialog.askstring('Read Aloud', 'Enter text to read aloud:')
            else:
                text = cmd[len('read aloud'):].strip()
            if not text:
                self.log('No text provided to read.')
                return
            self.log('Reading aloud...')
            self.status.config(text='Speaking')
            self.speak(text)
            self.status.config(text='Ready')

        elif low == 'exit' or low == 'quit':
            self.log('Exiting...')
            self.root.quit()

        else:
            self.log('Unrecognized command. Try: search, summarize, read aloud, calculate, open browser, exit')


if __name__ == '__main__':
    root = tk.Tk()
    app = VirtualAIGUI(root)
    root.mainloop()
