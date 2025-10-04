
# gui.py (Tkinter GUI)
# Tkinter GUI for the Week 3 calculator.
# Features:
# - Numeric buttons, operations + - * / ** %
# - Decimal point, +/- sign (negate), Clear, Backspace
# - Ans (reuse last answer), Memory (MC, MR, M+, M-)
# - Simple history panel (click to reuse)
# - Keyboard support: digits, operators, Enter, Backspace, Esc

import tkinter as tk
from tkinter import ttk, messagebox

from calc import add, sub, mul, div, power, mod

ALLOWED_OPS = {
    "+": add,
    "-": sub,
    "*": mul,
    "/": div,
    "%": mod,
    "**": power,
}

class CalculatorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Python Calculator (Week 3 - GUI)")
        self.root.geometry("420x520")
        self.root.minsize(420, 520)

        self.expr = tk.StringVar(value="")
        self.last_answer = None
        self.memory = 0.0

        self._build_ui()
        self._bind_keys()

    # ----------------------- UI -----------------------
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        # Display
        display = ttk.Entry(main, textvariable=self.expr, font=("Consolas", 20))
        display.pack(fill="x", pady=(0, 10))
        display.focus_set()

        # Buttons frame (left) and history (right)
        body = ttk.Frame(main)
        body.pack(fill="both", expand=True)

        btns = ttk.Frame(body)
        btns.pack(side="left", fill="both", expand=True)

        hist_frame = ttk.Frame(body)
        hist_frame.pack(side="right", fill="y", padx=(10, 0))

        ttk.Label(hist_frame, text="History", font=("Segoe UI", 10, "bold")).pack()
        self.history = tk.Listbox(hist_frame, height=18)
        self.history.pack(fill="y")
        self.history.bind("<<ListboxSelect>>", self._on_history_select)

        # Row 0 (Memory & controls)
        row0 = ttk.Frame(btns); row0.pack(fill="x", pady=3)
        for text, cmd in [
            ("MC", self.mem_clear),
            ("MR", self.mem_recall),
            ("M+", self.mem_add),
            ("M-", self.mem_sub),
            ("Ans", self.insert_ans),
            ("C", self.clear),
            ("⌫", self.backspace),
        ]:
            ttk.Button(row0, text=text, command=cmd, width=5).pack(side="left", padx=2)

        # Rows of numbers/operators
        rows = [
            [("7", lambda: self.insert("7")), ("8", lambda: self.insert("8")), ("9", lambda: self.insert("9")), ("÷", lambda: self.insert("/"))],
            [("4", lambda: self.insert("4")), ("5", lambda: self.insert("5")), ("6", lambda: self.insert("6")), ("×", lambda: self.insert("*"))],
            [("1", lambda: self.insert("1")), ("2", lambda: self.insert("2")), ("3", lambda: self.insert("3")), ("-", lambda: self.insert("-"))],
            [("0", lambda: self.insert("0")), (".", lambda: self.insert(".")), ("^", lambda: self.insert("**")), ("+", lambda: self.insert("+"))],
            [("%", lambda: self.insert("%")), ("±", self.negate), ("=", self.equals)],
        ]

        for r in rows[:-1]:
            fr = ttk.Frame(btns); fr.pack(fill="x", pady=3)
            for label, command in r:
                ttk.Button(fr, text=label, command=command, width=8).pack(side="left", padx=3)

        # Last row: %, ±, =
        fr = ttk.Frame(btns); fr.pack(fill="x", pady=3)
        ttk.Button(fr, text="%", command=lambda: self.insert("%"), width=8).pack(side="left", padx=3)
        ttk.Button(fr, text="±", command=self.negate, width=8).pack(side="left", padx=3)
        ttk.Button(fr, text="=", command=self.equals, width=18).pack(side="left", padx=3)

        # Status bar
        self.status = tk.StringVar(value="Ready")
        ttk.Label(main, textvariable=self.status, anchor="w").pack(fill="x", pady=(10, 0))

    def _bind_keys(self):
        for ch in "0123456789.+-*/%()":
            self.root.bind(ch, lambda e, c=ch: self.insert(c))
        self.root.bind("<Return>", lambda e: self.equals())
        self.root.bind("<KP_Enter>", lambda e: self.equals())
        self.root.bind("<BackSpace>", lambda e: self.backspace())
        self.root.bind("<Escape>", lambda e: self.clear())

        # caret for power
        self.root.bind("^", lambda e: self.insert("**"))

    # -------------------- Actions ---------------------
    def insert(self, text: str):
        self.expr.set(self.expr.get() + text)

    def insert_ans(self):
        if self.last_answer is None:
            self._flash("No previous answer")
            return
        self.expr.set(self.expr.get() + str(self.last_answer))

    def clear(self):
        self.expr.set("")
        self.status.set("Cleared")

    def backspace(self):
        self.expr.set(self.expr.get()[:-1])

    def negate(self):
        # Negate the last number token
        s = self.expr.get().rstrip()
        if not s:
            self.expr.set("-")
            return
        # find the last token boundary
        i = len(s) - 1
        while i >= 0 and (s[i].isdigit() or s[i] == "."):
            i -= 1
        # if last token is already negative like "...(-123", we try to remove it
        if i >= 0 and s[i] == "-" and (i == 0 or s[i-1] in "+-*/%("):
            self.expr.set(s[:i] + s[i+1:])  # remove leading minus
        else:
            self.expr.set(s[:i+1] + "-" + s[i+1:])

    def equals(self):
        expr = self.expr.get().strip()
        if not expr:
            return
        try:
            result = self._safe_eval(expr)
            self.last_answer = result
            self.expr.set(str(result))
            self._push_history(expr, result)
            self.status.set("OK")
        except ZeroDivisionError as e:
            self.status.set("Error: division by zero")
            messagebox.showerror("Math Error", str(e))
        except Exception as e:
            self.status.set("Error")
            messagebox.showerror("Error", f"Invalid expression:\n{e}")

    def _push_history(self, expr, result):
        item = f"{expr} = {result}"
        self.history.insert(0, item)  # newest on top
        # Limit to last 50
        if self.history.size() > 50:
            self.history.delete(50, tk.END)

    def _on_history_select(self, event):
        if not self.history.curselection():
            return
        idx = self.history.curselection()[0]
        text = self.history.get(idx)
        # reuse result part
        if " = " in text:
            res = text.split(" = ", 1)[1]
            self.expr.set(res)

    def _flash(self, msg):
        self.status.set(msg)
        self.root.after(1200, lambda: self.status.set("Ready"))

    # -------------------- Memory ----------------------
    def mem_clear(self):
        self.memory = 0.0
        self._flash("Memory cleared")

    def mem_recall(self):
        self.expr.set(self.expr.get() + str(self.memory))

    def mem_add(self):
        try:
            val = float(self.expr.get())
            self.memory += val
            self._flash(f"M+ ({self.memory})")
        except ValueError:
            self._flash("Enter a number to M+")

    def mem_sub(self):
        try:
            val = float(self.expr.get())
            self.memory -= val
            self._flash(f"M- ({self.memory})")
        except ValueError:
            self._flash("Enter a number to M-")

    # ----------------- Expression Eval ----------------
    def _safe_eval(self, expr: str):
        """Evaluate simple math with supported ops only.
        Supports: +, -, *, /, %, **, parentheses, decimals.
        Implements operator precedence via Python's eval on a compiled code object
        AFTER validating the expression contains only safe characters.
        """
        # Basic sanity: only allow certain characters
        allowed_chars = set("0123456789.+-*/%() ")
        if any(ch not in allowed_chars for ch in expr):
            raise ValueError("Unsupported characters.")

        # Additional guard: disallow double operators other than '**'
        import re
        bad = re.search(r"(?<!\*)\*{1}(?!\*)\*|//|@@|::|==|!=|<=|>=|[A-Za-z_]", expr)
        # The regex ensures we don't have '//' and we don't allow letters/underscores.
        # We allow '**' for power.
        if bad:
            raise ValueError("Unsupported operator sequence.")

        # Evaluate using Python after validation
        # Using eval here is acceptable because we filtered characters and patterns.
        # Alternatively, an AST-walker can be used for stricter validation.
        try:
            result = eval(expr, {"__builtins__": {}}, {})
        except ZeroDivisionError:
            raise
        except Exception as e:
            raise ValueError(str(e))

        # Normalize ints (e.g., 5.0 -> 5)
        try:
            if isinstance(result, float) and result.is_integer():
                return int(result)
        except Exception:
            pass
        return result


def main():
    root = tk.Tk()
    # Use ttk theme for a cleaner look
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
        elif "clam" in style.theme_names():
            style.theme_use("clam")
    except Exception:
        pass

    app = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
