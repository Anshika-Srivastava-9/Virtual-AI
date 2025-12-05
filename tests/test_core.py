import sys
import os
import pytest

# Ensure repository root is on sys.path so tests can import the module
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import virtual_ai_gui as va


def test_summarize_local_short():
    text = "Short sentence."
    assert va.summarize_text_local(text, max_sentences=2) == "Short sentence."


def test_summarize_local_extracts_top_sentences():
    text = (
        "Apple is a fruit. "
        "Car engines are complex machines. "
        "Bananas are yellow and sweet. "
        "Automobiles require fuel."
    )
    summary = va.summarize_text_local(text, max_sentences=2)
    assert isinstance(summary, str)
    # summary should contain two sentences from the input
    parts = [s.strip() for s in summary.split('.') if s.strip()]
    assert 1 <= len(parts) <= 2


def test_safe_eval_valid():
    assert va.safe_eval('2+3*4') == 14
    assert va.safe_eval('10/2') == 5.0


def test_safe_eval_rejects_letters():
    with pytest.raises(ValueError):
        va.safe_eval('os.system("ls")')


def test_safe_eval_disallows_calls():
    with pytest.raises(ValueError):
        va.safe_eval('__import__("os").system("ls")')
