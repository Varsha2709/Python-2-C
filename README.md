
# 🔧 Python-to-C Compiler (CLI-Based)

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

## 📁 Project Structure

```bash
.
├── lexical_analysis.py     # Token extraction
├── syntax_analysis.py      # AST parsing and error checking
├── semantic_analysis.py    # Unreachable code, semantic warnings
├── tac_generation.py       # Three Address Code generation
├── translator.py           # Python to C translation
├── optimizer.py            # Code optimization, loop invariants
├── main.py                 # Integration and CLI interface
```

## 📚 Educational Use

This project is perfect for:

* Compiler design assignments
* Understanding translation from high-level to low-level code
* Research on static analysis and IR generation


