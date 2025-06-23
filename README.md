
# 🔧 Python-to-C Compiler 

A modular  tool that simulates the **phases of a compiler** and converts generalized Python code into optimized C code. This project is built with a focus on **learning**, **code translation**, and **compiler design concepts**—ideal for students, developers, and researchers.

---

## 🚀 Features

* ✅ **Lexical Analysis**
  Extracts tokens using regex and identifies syntax units from the input Python code.

* 🧠 **Syntax Analysis**
  Uses Python’s AST module to parse and validate code structure.

* 🧩 **Semantic Analysis**
  Detects unreachable code, insecure constructs (like `eval`), and semantic issues.

* 🔃 **Three Address Code (TAC) Generation**
  Converts arithmetic and assignment expressions into TAC format.

* 🔁 **Python-to-C Translation**
  Translates constructs like `print`, `if`, `for`, `while`, and basic expressions to equivalent C code.

* 🚀 **Code Optimization**
  Performs **loop-invariant code motion** and identifies **basic blocks** for better code structure and performance.

---



### 📦 Requirements

* Python 3.x (No external libraries needed)

### ▶️ Run the Compiler

```bash
python main.py
```

This will:

1. Perform all compiler phases
2. Output intermediate and final translated C code
3. Show optimizations in-place

---

Absolutely, Varsha! Here's how to turn your Python-to-C compiler into a **command-line tool** 🚀

---

## ✅ Step-by-Step CLI Tool Structure

### 📁 Directory Structure

```
python_to_c_compiler/
├── compiler.py        # Main compiler logic (your current code)
├── cli.py             # CLI interface (entry point)
├── py2c_gui.py        # GUI interface (entry point)
├── sample.py          # (optional) Example Python code
```

---

### 🧠 `compiler.py` – Main Logic (modularized)

We split your code into **functions** that can be called from the CLI or GUI app:

```python
# compiler.py
import ast
import re

def lexical_analysis(code): ...
def check_syntax(code): ...
def semantic_analysis(code): ...
def generate_TAC(code): ...
def translate_python_to_c(code): ...
def optimize_c_code(code): ...

def compile_all(code):
    lexical_analysis(code)
    check_syntax(code)
    semantic_analysis(code)
    generate_TAC(code)
    c_code = translate_python_to_c(code)
    optimized = optimize_c_code(c_code)
    return optimized
```

---


### ✅ How to Run It

1. **Save files:**

   * Put the above into `compiler.py` and `cli.py`

2. **Make executable:**

```bash
chmod +x cli.py
```

3. **Run it from terminal:**
   For CLI
```bash
python cli.py sample.py -o translated.c
```
 For GUI 
```bash
python p2c_gui.py

```

> `sample.py` is your Python file. The output will be written to `translated.c`.

---

### 📦 Make It Installable as a CLI Tool

Create a `setup.py` if you want to install it:

```python
from setuptools import setup

setup(
    name="py2ccompiler",
    version="1.0",
    py_modules=["cli", "compiler"],
    entry_points={
        "console_scripts": ["py2c=cli:main"]
    },
)
```

Then install:

```bash
pip install .
py2c sample.py -o translated.c
```

## 📚 Educational Use

This project is perfect for:

* Compiler design assignments
* Understanding translation from high-level to low-level code
* Research on static analysis and IR generation


