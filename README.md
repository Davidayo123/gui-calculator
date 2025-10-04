
# Week 3 — Python Calculator (CLI + Tkinter GUI)

This folder contains a **clean CLI calculator** and a **Tkinter GUI calculator**.

## Features
- Operations: `+  -  *  /  **  %`
- Reuse last answer in CLI (`ans`)
- GUI extras: **memory keys (MC/MR/M+/M-)**, **Ans**, **history list**, **±**, **backspace**, keyboard support

## Structure
```
calculator_week3_gui/
├─ calc.py          # pure math functions
├─ main.py          # CLI calculator
├─ gui.py           # Tkinter GUI
└─ tests/
   └─ test_calc.py  # optional pytest tests
```

## Run (CLI)
```bash
python main.py
```

## Run (GUI)
```bash
python gui.py
```

> **Note (Linux):** you may need to install Tk support for Python, e.g. `sudo apt-get install python3-tk`.

## Test (optional)
```bash
pip install pytest
pytest -q
```
