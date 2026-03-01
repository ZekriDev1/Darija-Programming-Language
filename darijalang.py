import sys
import re
import os
import traceback

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def load_sintax(file_path):
    mappings = {}
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if ' = ' in line:
                    d, p = line.split(' = ', 1)
                    d_strip = d.strip()
                    if d_strip:
                        if d_strip != p.strip():
                            mappings[d_strip] = p.strip()
                elif '=' in line:
                    d, p = line.split('=', 1)
                    d_strip = d.strip()
                    if d_strip:
                        if d_strip != p.strip():
                            mappings[d_strip] = p.strip()
    except Exception:
        return {}
    return mappings

def translate_line(line, mappings, keywords):
    indent_match = re.match(r'^(\s*)', line)
    indent = indent_match.group(1) if indent_match else ""
    content = line[len(indent):]
    
    if not content or content.startswith('#'):
        return line

    func_pattern = r'^(3rf)\s+([a-zA-Z0-9_]+)\s*\((.*)\)\s*:'
    match = re.search(func_pattern, content)
    if match:
        func_keyword = match.group(1)
        func_name = match.group(2)
        if func_name[0].isdigit():
            func_name = "_" + func_name
        params_str = match.group(3)
        
        translated_params = []
        if params_str.strip():
            for p in params_str.split(','):
                p_clean = p.strip()
                if p_clean == 'rassi':
                    translated_params.append('self')
                    continue
                
                parts = p_clean.split()
                if len(parts) == 2:
                    t, n = parts
                    t_py = mappings.get(t, t)
                    translated_params.append(f"{n}: {t_py}")
                else:
                    p_replaced = p_clean
                    for k in keywords:
                        if k == mappings[k]: continue
                        pattern = r'(?<![a-zA-Z0-9_])' + re.escape(k) + r'(?![a-zA-Z0-9_])'
                        p_replaced = re.sub(pattern, mappings[k], p_replaced)
                    translated_params.append(p_replaced)
        
        return f"{indent}def {func_name}({', '.join(translated_params)}):"

    string_pattern = r'(".*?"|\'.*?\')'
    parts = re.split(string_pattern, content)
    new_parts = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            part = re.sub(r'(\w+)\+\+', r'\1 += 1', part)
            part = re.sub(r'(\w+)\-\-', r'\1 -= 1', part)

            for k in keywords:
                if k == mappings[k]:
                    continue
                pattern = r'(?<![a-zA-Z0-9_])' + re.escape(k) + r'(?![a-zA-Z0-9_])'
                part = re.sub(pattern, mappings[k], part)
            
            part = re.sub(r'\b(\d[a-zA-Z0-9_]*[a-zA-Z_][a-zA-Z0-9_]*)\b', r'_\1', part)
            
            new_parts.append(part)
        else:
            new_parts.append(part)
    
    return indent + "".join(new_parts)

def get_darija_error(exception):
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
        print(f"{Color.YELLOW}Isti3mal: python darijalang.py <file.darija>{Color.RESET}")
        sys.exit(1)

    daria_file = sys.argv[1]
    if not os.path.exists(daria_file):
        print(f"{Color.RED}{Color.BOLD}L-mlaf '{daria_file}' ma kaynx!{Color.RESET}")
        sys.exit(1)

    mappings = load_sintax("sintax.txt")
    if not mappings:
        mappings = {
            "3rf": "def", "weri": "print", "rj3": "return", 
            "ila": "if", "awla": "else", "htta": "while", "3la": "for"
        }

    keywords = sorted(mappings.keys(), key=len, reverse=True)

    try:
        with open(daria_file, 'r', encoding='utf-8') as f:
            daria_lines = f.readlines()

        python_lines = []
        for line in daria_lines:
            python_lines.append(translate_line(line, mappings, keywords))

        python_code = "\n".join(python_lines)

        global_scope = {
            "__name__": "__main__",
            "__builtins__": __builtins__,
            "color_bold": Color.BOLD,
            "color_reset": Color.RESET,
            "color_7mer": Color.RED,
            "color_khder": Color.GREEN,
            "color_sfer": Color.YELLOW,
            "color_zreq": Color.BLUE,
            "color_smawi": Color.CYAN,
        }
        
        try:
            exec(python_code, global_scope)
        except Exception as e:
            print("\n" + Color.RED + "!" * 40 + Color.RESET)
            print(f"{Color.RED}{Color.BOLD}TKHASRET L-OMOUR (Runtime Error):{Color.RESET}")
            print(f"{Color.CYAN}{get_darija_error(e)}{Color.RESET}")
            print(Color.RED + "-" * 40 + Color.RESET)
            tb = traceback.extract_tb(sys.exc_info()[2])
            for entry in reversed(tb):
                if entry.filename == '<string>':
                    line_no = entry.lineno
                    if 0 < line_no <= len(daria_lines):
                        print(f"{Color.YELLOW}L-khata2 f l-star {line_no}:{Color.RESET}")
                        print(f"  > {Color.BOLD}{daria_lines[line_no-1].strip()}{Color.RESET}")
                    break
            print(Color.RED + "!" * 40 + Color.RESET)

    except Exception as e:
        print(f"Mochkil fi l-qira2a dial l-mlaf: {e}")

if __name__ == "__main__":
    main()
