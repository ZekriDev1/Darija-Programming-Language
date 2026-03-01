import sys
import re
import os
import traceback

def load_sintax(file_path):
    """Load mappings from sintax.txt."""
    mappings = {}
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                # Use split by ' = ' to handle cases where '=' is the keyword
                if ' = ' in line:
                    d, p = line.split(' = ', 1)
                    d_strip = d.strip()
                    if d_strip:
                        mappings[d_strip] = p.strip()
                elif '=' in line: # Fallback
                    d, p = line.split('=', 1)
                    d_strip = d.strip()
                    if d_strip:
                        mappings[d_strip] = p.strip()
    except Exception:
        return {}
    return mappings

def translate_line(line, mappings, keywords):
    """Translate a single line of DarijaLang to Python."""
    # Preserve indentation
    indent_match = re.match(r'^(\s*)', line)
    indent = indent_match.group(1) if indent_match else ""
    content = line[len(indent):]
    
    # Skip empty lines or comments
    if not content or content.startswith('#'):
        return line

    # 1. Handle function and class signatures specifically
    # 3rf func_name(klma name, ra9m age):
    func_pattern = r'^(3rf)\s+(\w+)\s*\((.*)\)\s*:'
    match = re.search(func_pattern, content)
    if match:
        func_keyword = match.group(1)
        func_name = match.group(2)
        params_str = match.group(3)
        
        translated_params = []
        if params_str.strip():
            for p in params_str.split(','):
                p_clean = p.strip()
                # Special case: rassi (self)
                if p_clean == 'rassi':
                    translated_params.append('self')
                    continue
                
                # Check for type annotation: 'klma name' -> 'name: str'
                parts = p_clean.split()
                if len(parts) == 2:
                    t, n = parts
                    t_py = mappings.get(t, t)
                    translated_params.append(f"{n}: {t_py}")
                else:
                    # Just replace keywords in param name if any (unlikely for param name but stay safe)
                    p_replaced = p_clean
                    for k in keywords:
                        # Use word boundaries that include numbers like 3, 7, 9
                        pattern = r'(?<![0-9a-zA-Z_])' + re.escape(k) + r'(?![0-9a-zA-Z_])'
                        p_replaced = re.sub(pattern, mappings[k], p_replaced)
                    translated_params.append(p_replaced)
        
        return f"{indent}def {func_name}({', '.join(translated_params)}):"

    # 2. Handle generic replacements outside of strings
    # We split by strings to avoid replacing keywords inside quotes
    string_pattern = r'(".*?"|\'.*?\')'
    parts = re.split(string_pattern, content)
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Not in a string
            # Apply all keyword mappings
            for k in keywords:
                # If d == p, no need to replace (like + = +)
                if k == mappings[k]:
                    continue
                pattern = r'(?<![0-9a-zA-Z_])' + re.escape(k) + r'(?![0-9a-zA-Z_])'
                part = re.sub(pattern, mappings[k], part)
            new_parts.append(part)
        else:  # Inside a string
            new_parts.append(part)
    
    return indent + "".join(new_parts)

def get_darija_error(exception):
    """Attempt to provide a Darija-friendly context for errors."""
    err_type = type(exception).__name__
    
    translations = {
        'NameError': 'Smiya ma m3rofach (Variable undefined)',
        'TypeError': 'No3 dial l-mo3طayat machi hwa hadak (Type error)',
        'ValueError': 'L-qima ghalata (Value error)',
        'SyntaxError': 'L-ktiba fiha moxkil (Syntax error)',
        'ZeroDivisionError': 'Ma ymknch tqsm 3la sifr (Division by zero)',
        'IndexError': 'L-indeks ma kaynx f l-lista (Index out of range)',
        'KeyError': 'L-sarout ma kaynx f l-m3qad (Key not found)',
        'ModuleNotFoundError': 'Had l-modul ma msetelch (Module not found)',
        'FileNotFoundError': 'Had l-mlaf ma kaynx (File not found)',
        'PermissionError': 'Ma 3ndekx l-7aq tqra had l-mlaf (Permission denied)',
    }
    
    msg = translations.get(err_type, err_type)
    return f"Mochkil: {msg}\n{str(exception)}"

def main():
    if len(sys.argv) < 2:
        print("Isti3mal: python darijalang.py <file.daria>")
        sys.exit(1)

    daria_file = sys.argv[1]
    if not os.path.exists(daria_file):
        print(f"L-mlaf '{daria_file}' ma kaynx!")
        sys.exit(1)

    # 1. Load mappings
    mappings = load_sintax("sintax.txt")
    if not mappings:
        # Fallback basic mappings if file missing or empty
        mappings = {
            "3rf": "def", "weri": "print", "rj3": "return", 
            "ila": "if", "awla": "else", "htta": "while", "3la": "for"
        }

    # Keywords sorted by length (longest first to catch "awla ila" before "awla")
    keywords = sorted(mappings.keys(), key=len, reverse=True)

    # 2. Read and translate code
    try:
        with open(daria_file, 'r', encoding='utf-8') as f:
            daria_lines = f.readlines()

        python_lines = []
        for line in daria_lines:
            python_lines.append(translate_line(line, mappings, keywords))

        python_code = "\n".join(python_lines)

        # 3. Execute the code
        # We define a custom 'print' that can be replaced if needed, but 'weri' already maps to 'print'
        
        global_scope = {
            "__name__": "__main__",
            "__builtins__": __builtins__
        }
        
        try:
            exec(python_code, global_scope)
        except Exception as e:
            print("\n" + "!" * 40)
            print("TKHASRET L-OMOUR (Runtime Error):")
            print(get_darija_error(e))
            print("-" * 40)
            # Show the line that caused the error in DarijaLang if possible
            tb = traceback.extract_tb(sys.exc_info()[2])
            # The last entry usually points to the executed code
            for entry in reversed(tb):
                if entry.filename == '<string>':
                    line_no = entry.lineno
                    if 0 < line_no <= len(daria_lines):
                        print(f"L-khata2 f l-star {line_no}:")
                        print(f"  > {daria_lines[line_no-1].strip()}")
                    break
            print("!" * 40)

    except Exception as e:
        print(f"Mochkil fi l-qira2a dial l-mlaf: {e}")

if __name__ == "__main__":
    main()
