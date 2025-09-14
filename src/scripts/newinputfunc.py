from functools import cache
import numpy as np
import re

def safe_ln(n: int):
    if (n > 0):
        return np.log(n)
    else:
        raise ValueError

def safe_log(n: int):
    if (n > 0):
        return np.log10(n)
    else:
        raise ValueError

def safe_sqrt(n: int):
    if (n >= 0):
        return np.sqrt(n)
    else:
        raise ValueError

SAFE_NAMES = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "log": safe_log,
    "ln": safe_ln,
    "sqrt": safe_sqrt,
    "abs": np.abs,
    "pi": np.pi,
    "e": np.e,
}

def math_filter(func: str, x: float) -> str:
    func = func.replace("sen", "sin")
    func = re.sub(r'(\d|\))x', r'\1*x', func)
    func = re.sub(r'(\d|x|\))\(', r'\1*(', func)
    func = re.sub(r'\)(\d|x)', r')*\1', func)
    func = re.sub(r'(\d|x)(?=(sin|cos|tan|log|ln|sqrt)\()', r'\1*', func)
    func = func.replace("x", f"({x})")
    func = func.replace("^", "**")
    func = re.sub(r"\|\s*([^|]+?)\s*\|", r"abs(\1)", func)
    return func

@cache
def custom_eval(func: str, x: float):
    result: float = -1
    mod_input = math_filter(func, x)
    try:
        result = np.round(eval(mod_input, {"__builtins__": None}, SAFE_NAMES), 10)
        return result
    except Exception as e:
        raise ValueError
    
if __name__ == "__main__":
    res = custom_eval("sqrt(x)", -1)
    print(res)