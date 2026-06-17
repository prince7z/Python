def read_file(path):
    """Read a file's contents."""
    try:
        with open(path, "r") as f:
            content = f.read()
        return json.dumps({"path": path, "content": content[:3000], "truncated": len(content) > 3000})
    except Exception as e:
        return json.dumps({"error": str(e)})

def write_file(path, content):
    """Write content to a file."""
    try:
        d = os.path.dirname(path)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(path, "w") as f:
            f.write(content)
        return json.dumps({"status": "success", "path": path, "bytes": len(content)})
    except Exception as e:
        return json.dumps({"error": str(e)})

def run_python(code):
    """Execute Python code and return stdout/stderr."""
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True, text=True, timeout=15,
        )
        return json.dumps({
            "stdout": result.stdout[:2000] if result.stdout else "",
            "stderr": result.stderr[:2000] if result.stderr else "",
            "exit_code": result.returncode,
        })
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "Timed out (15s limit)"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def list_files(path="."):
    """List files in a directory."""
    try:
        items = sorted(os.listdir(path))
        return json.dumps({"path": path, "files": items[:50]})
    except Exception as e:
        return json.dumps({"error": str(e)})
def calculate_math(expression):
    """Safely evaluate a math expression."""
    try:
        allowed = set("0123456789+-*/.() eE")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": f"Invalid characters in: {expression}"})
        result = eval(expression)
        return json.dumps({"expression": expression, "result": round(result, 6)})
    except Exception as e:
        return json.dumps({"error": str(e)})

CODE_TOOLS = {
    "read_file": {"fn": read_file, "desc": "read_file(path: str) — Read a file and return its contents."},
    "write_file": {"fn": write_file, "desc": 'write_file(path: str, content: str) — Write content to a file.'},
    "run_python": {"fn": run_python, "desc": "run_python(code: str) — Execute Python code. Returns stdout/stderr."},
    "list_files": {"fn": list_files, "desc": "list_files(path: str) — List files in a directory."},
    "calculate": {"fn": calculate_math, "desc": "calculate(expression: str) — Evaluate a math expression."},
}


print(f"Code tools: {list(CODE_TOOLS.keys())}")

