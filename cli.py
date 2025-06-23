# cli.py
import argparse
from compiler import compile_all

def main():
    parser = argparse.ArgumentParser(description="🛠 Python to C Compiler with Compilation Phases")
    parser.add_argument("input", help="Path to Python (.py) source file")
    parser.add_argument("-o", "--output", help="Output C file path", default="output.c")
    args = parser.parse_args()

    try:
        with open(args.input, "r") as file:
            code = file.read()
        c_code = compile_all(code)
        with open(args.output, "w") as file:
            file.write(c_code)
        print(f"✅ C code written to {args.output}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
