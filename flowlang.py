import io
import sys

variables = {}
functions = {}

def evaluate_expression(expr):
    try:
        for var in variables:
            expr = expr.replace(var, str(variables[var]))
        return eval(expr)
    except Exception as e:
        return f"Error: {e}"

def run_block(lines, i):
    block = []
    while i < len(lines) and lines[i].strip() != "end":
        block.append(lines[i])
        i += 1
    return block, i

def run_lines(lines):
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        if line.startswith("let "):
            _, rest = line.split("let ", 1)
            var, expr = rest.split("=", 1)
            var = var.strip()
            value = evaluate_expression(expr.strip())
            variables[var] = value

        elif line.startswith("show "):
            expr = line[5:].strip()
            print(evaluate_expression(expr))

        elif line.startswith("if "):
            condition = line[3:].strip()
            result = evaluate_expression(condition)
            block, i = run_block(lines, i + 1)
            i += 1
            if result:
                run_lines(block)
            elif i < len(lines) and lines[i].strip() == "else":
                else_block, i = run_block(lines, i + 1)
                i += 1
                run_lines(else_block)

        elif line.startswith("repeat "):
            parts = line.split()
            if "times" in parts:
                count = int(evaluate_expression(parts[1]))
                block, i = run_block(lines, i + 1)
                i += 1
                for _ in range(count):
                    run_lines(block)

        elif line.startswith("func "):
            func_def = line[5:]
            if "(" in func_def and ")" in func_def:
                name = func_def.split("(")[0].strip()
                params = func_def.split("(")[1].split(")")[0].split(",")
                params = [p.strip() for p in params if p.strip()]
                block, i = run_block(lines, i + 1)
                i += 1
                functions[name] = (params, block)

        elif "(" in line and ")" in line:
            name = line.split("(")[0].strip()
            args = line.split("(")[1].split(")")[0].split(",")
            args = [evaluate_expression(arg.strip()) for arg in args if arg.strip()]
            if name in functions:
                params, block = functions[name]
                if len(params) == len(args):
                    backup = variables.copy()
                    for p, a in zip(params, args):
                        variables[p] = a
                    run_lines(block)
                    variables.update(backup)

        i += 1

def run_code(code):
    code_lines = code.splitlines()
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        run_lines(code_lines)
        output = sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout
    return output