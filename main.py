
# main.py (CLI)
from calc import add, sub, mul, div, power, mod

BANNER = """
=============================
     Python CLI Calculator
=============================
Ops: +  -  *  /  **  %
Type 'ans' to reuse last result, 'q' to quit.
"""

def parse_number(prompt, last_ans):
    while True:
        raw = input(prompt).strip().lower()
        if raw == "ans":
            if last_ans is None:
                print("No previous answer yet.")
                continue
            return last_ans
        try:
            return float(raw)
        except ValueError:
            print("Please enter a number (or 'ans').")

def pick_op():
    ops = {"+": add, "-": sub, "*": mul, "/": div, "**": power, "%": mod}
    while True:
        op = input("Choose operation (+ - * / ** %): ").strip()
        if op in ops:
            return op, ops[op]
        print("Invalid op. Use one of: + - * / ** %")

def main():
    print(BANNER)
    last = None
    while True:
        cmd = input("Press Enter to start, or 'q' to quit: ").strip().lower()
        if cmd == "q":
            print("Goodbye!")
            break

        a = parse_number("Enter first number: ", last)
        op_symbol, fn = pick_op()
        b = parse_number("Enter second number: ", last)

        try:
            result = fn(a, b)
            print(f"Result: {a} {op_symbol} {b} = {result}")
            last = result
        except ZeroDivisionError as e:
            print("Error:", e)
        except Exception as e:
            print("Unexpected error:", e)

if __name__ == "__main__":
    main()
