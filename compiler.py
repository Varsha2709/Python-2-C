import ast
import re

# -------------------------
# Lexical Analysis
# -------------------------
def lexical_analysis(code):
    print("🔍 Lexical Analysis:")
    tokens = re.findall(r'\b\w+\b|[^\s\w]', code)
    print("Tokens:", tokens)
    print("-" * 50)
    return tokens

# -------------------------
# Syntax Analysis
# -------------------------
def check_syntax(code):
    print("🧠 Syntax Analysis:")
    try:
        tree = ast.parse(code)
        print("✔ No syntax errors.")
    except SyntaxError as e:
        print(f"❌ Syntax Error: {e}")
    print("-" * 50)
    return tree

# -------------------------
# Semantic Analysis
# -------------------------
class UnreachableCodeVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        has_return = False
        for stmt in node.body:
            if has_return:
                print(f"⚠ Unreachable code at line {stmt.lineno}")
            if isinstance(stmt, ast.Return):
                has_return = True
        self.generic_visit(node)

def semantic_analysis(code):
    print("🧩 Semantic Analysis:")
    tree = ast.parse(code)
    UnreachableCodeVisitor().visit(tree)
    if "eval(" in code or "exec(" in code:
        print("⚠ Warning: Use of eval/exec is insecure.")
    print("-" * 50)

# -------------------------
# Three Address Code (TAC)
# -------------------------
temp_count = 0
def get_temp():
    global temp_count
    t = f"t{temp_count}"
    temp_count += 1
    return t

def generate_TAC(code):
    print("🔃 Three Address Code (TAC):")
    tree = ast.parse(code)
    tac_lines = []

    class TACVisitor(ast.NodeVisitor):
        def visit_Assign(self, node):
            if isinstance(node.value, ast.BinOp):
                left = getattr(node.value.left, 'id', getattr(node.value.left, 'n', '?'))
                right = getattr(node.value.right, 'id', getattr(node.value.right, 'n', '?'))
                op = type(node.value.op).__name__
                op_map = {'Add': '+', 'Sub': '-', 'Mult': '*', 'Div': '/'}
                temp = get_temp()
                tac_lines.append(f"{temp} = {left} {op_map.get(op, '?')} {right}")
                tac_lines.append(f"{node.targets[0].id} = {temp}")
            elif isinstance(node.value, ast.Constant):
                tac_lines.append(f"{node.targets[0].id} = {node.value.value}")

    TACVisitor().visit(tree)
    for line in tac_lines:
        print(line)
    print("-" * 50)

# -------------------------
# Python to C Translator
# -------------------------
def translate_python_to_c(code):
    print("🔁 Python to C Translation:")
    lines = code.strip().split('\n')
    translated = ['#include <stdio.h>', '#include <math.h>', '']
    indent_level = 0
    declared_vars = {}

    indent = lambda: "    " * indent_level

    for line in lines:
        original = line
        line = re.sub(r"(\w+)\s*\*\*\s*(\w+)", r"pow(\1, \2)", line)  # exponentiation
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Function definition
        if stripped.startswith("def "):
            func = re.match(r"def (\w+)\((.*?)\):", stripped)
            if func:
                name, args = func.groups()
                args_c = ", ".join([f"int {a.strip()}" for a in args.split(",") if a.strip()])
                translated.append(f"{indent()}int {name}({args_c}) {{")
                indent_level += 1

        # Return
        elif stripped.startswith("return"):
            val = stripped[len("return"):].strip()
            val = "1" if val == "True" else "0" if val == "False" else val
            translated.append(f"{indent()}return {val};")

        # if / elif / else
        elif stripped.startswith("if "):
            cond = stripped[3:].rstrip(":").replace("and", "&&").replace("or", "||").replace("not", "!")
            translated.append(f"{indent()}if ({cond}) {{")
            indent_level += 1
        elif stripped.startswith("elif "):
            indent_level -= 1
            cond = stripped[5:].rstrip(":").replace("and", "&&").replace("or", "||").replace("not", "!")
            translated.append(f"{indent()}}} else if ({cond}) {{")
            indent_level += 1
        elif stripped.startswith("else"):
            indent_level -= 1
            translated.append(f"{indent()}}} else {{")
            indent_level += 1

        # while loop
        elif stripped.startswith("while "):
            cond = stripped[6:].rstrip(":")
            translated.append(f"{indent()}while ({cond}) {{")
            indent_level += 1

        # for loop (range)
        elif "for " in stripped and "in range(" in stripped:
            match = re.match(r"for (\w+) in range\((.*?)\):", stripped)
            if match:
                var, expr = match.groups()
                parts = [p.strip() for p in expr.split(",")]
                if len(parts) == 1:
                    translated.append(f"{indent()}for (int {var} = 0; {var} < {parts[0]}; {var}++) {{")
                elif len(parts) == 2:
                    translated.append(f"{indent()}for (int {var} = {parts[0]}; {var} < {parts[1]}; {var}++) {{")
                elif len(parts) == 3:
                    translated.append(f"{indent()}for (int {var} = {parts[0]}; {var} < {parts[1]}; {var} += {parts[2]}) {{")
                indent_level += 1

        # Input handling
        elif "input(" in stripped:
            match = re.match(r"(\w+)\s*=\s*int\s*\(\s*input\s*\((.*)\)\s*\)", stripped)
            if match:
                var, prompt = match.groups()
                prompt = prompt.strip().strip('"').strip("'")
                translated.append(f'{indent()}printf("{prompt}");')
                translated.append(f'{indent()}scanf("%d", &{var});')
                declared_vars[var] = "int"

        # print with f-string
        elif stripped.startswith("print(f"):
            inner = stripped[7:-1]
            fmt = re.sub(r"\{(\w+)\}", r"%d", inner)
            args = ", ".join(re.findall(r"\{(\w+)\}", inner))
            translated.append(f'{indent()}printf("{fmt}\\n", {args});')

        # print regular
        elif stripped.startswith("print("):
            val = stripped[6:-1].strip()
            if val.startswith('"') or val.startswith("'"):
                val = val.strip('"').strip("'")
                translated.append(f'{indent()}printf("{val}\\n");')
            else:
                fmt = "%d" if declared_vars.get(val) == "int" else "%f"
                translated.append(f'{indent()}printf("{fmt}\\n", {val});')

        # Variable assignment
        elif "=" in stripped:
            var, val = [x.strip() for x in stripped.split("=", 1)]
            if var not in declared_vars:
                if re.match(r"^\d+$", val):
                    declared_vars[var] = "int"
                    translated.append(f"{indent()}int {var} = {val};")
                elif re.match(r"^\d+\.\d+$", val):
                    declared_vars[var] = "float"
                    translated.append(f"{indent()}float {var} = {val};")
                elif val in ["True", "False"]:
                    declared_vars[var] = "bool"
                    translated.append(f"{indent()}bool {var} = {1 if val == 'True' else 0};")
                else:
                    translated.append(f"{indent()}// Unsupported assignment: {original}")
            else:
                translated.append(f"{indent()}{var} = {val};")

        # pass
        elif stripped == "pass":
            translated.append(f"{indent()}// pass")

        # block end
        elif not original.startswith(" ") and indent_level > 0:
            indent_level -= 1
            translated.append(f"{indent()}}}")

        # fallback
        else:
            translated.append(f"{indent()}// Unsupported: {stripped}")

    while indent_level > 0:
        indent_level -= 1
        translated.append(f"{indent()}}}")

    print("\n".join(translated))
    print("-" * 50)
    return "\n".join(translated)

# -------------------------
# Code Optimization
# -------------------------
def optimize_c_code(code):
    print("🚀 Optimized C Code:")
    lines = code.split('\n')
    optimized = [line for line in lines if line.strip() and line.strip() != ";"]
    print("\n".join(optimized))
    print("-" * 50)
    return "\n".join(optimized)

# -------------------------
# Sample Python Code
# -------------------------
sample_code = """
# Function to check if a number is prime
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

number = int(input("Enter a number: "))

if is_prime(number):
    print(f"{number} is a prime number.")
else:
    print(f"{number} is not a prime number.")
"""

# -------------------------
# Full Compilation Pipeline
# -------------------------
lexical_analysis(sample_code)
check_syntax(sample_code)
semantic_analysis(sample_code)
generate_TAC(sample_code)
c_code = translate_python_to_c(sample_code)
optimize_c_code(c_code)
