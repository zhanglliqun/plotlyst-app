import os
import ast
import re

def find_py_files(directory):
    """Find all .py files in a directory."""
    py_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

def is_likely_translatable(s):
    """
    Heuristics to determine if a string is likely user-facing text.
    """
    if not s or not s.strip():
        return False
    # Filter out Qt StyleSheets
    if any(keyword in s for keyword in ['{', '}', ':', ';', 'px', 'border', 'color', 'background-color']):
        return False
    # Must contain at least one space, likely a sentence
    if ' ' not in s:
        return False
    # Filter out docstrings or code snippets
    if any(keyword in s for keyword in ['def ', 'class ', 'import ', 'return ']):
        return False
    # Filter out paths and URLs
    if '/' in s or 'http' in s or 'www' in s:
        return False
    # Filter out short, noisy strings
    if len(s.strip()) < 5:
        return False
    # Must start with a capital letter (common for UI text)
    if not s.strip()[0].isupper():
        return False
    return True

def extract_strings_from_py(file_path):
    """Extract translatable strings from a Python file using AST."""
    strings = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    s = node.value
                    if is_likely_translatable(s):
                        strings.add(s.strip())
        except (SyntaxError, ValueError) as e:
            print(f"Warning: Could not parse {file_path}: {e}")
    return strings

if __name__ == '__main__':
    py_directory = 'src/main/python/plotlyst/view/'
    all_strings = set()
    py_files = find_py_files(py_directory)
    for file in py_files:
        all_strings.update(extract_strings_from_py(file))

    sorted_strings = sorted(list(all_strings))

    print("Found translatable strings in Python files:")
    for s in sorted_strings:
        print(s)
