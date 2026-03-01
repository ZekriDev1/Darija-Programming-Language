# 🇲🇦 DarijaLang

**DarijaLang** is a custom programming language that allows you to write code using Moroccan Darija keywords. It maps Darija terms directly to their Python equivalents, providing a fun and culturally resonant way for Moroccans to explore programming.

The project includes both a **Python-based interpreter** and a **VS Code extension** for syntax highlighting and a better developer experience.

---

## 🚀 Features

-   **Darija Keywords**: Use terms like `3rf` (def), `weri` (print), and `ila` (if) to write your logic.
-   **Easy Execution**: Run any `.darija` file directly using the Python interpreter.
-   **VS Code Support**: Custom extension with syntax highlighting, auto-indentation, and a dedicated language icon.
-   **Informative Errors**: Error messages are translated into Darija contexts (e.g., `Smiya ma m3rofach` for NameError).
-   **Full Python Power**: Since it's built on Python, you have access to lists, integers, functions, and more.

---

## 🛠️ Getting Started

### 1. Requirements
Ensure you have **Python 3.x** installed on your system.

### 2. File Structure
- `darijalang.py`: The interpreter.
- `sintax.txt`: Contains keyword mappings.
- `main.daria`: Your Darija source code.
- `darijalang-extension/`: VS Code extension folder.

### 3. Run a Program
To execute a DarijaLang file:
```powershell
python darijalang.py main.daria
```

---

## 📝 Syntax Reference

### Control Flow
| Darija | Python | Description |
| :--- | :--- | :--- |
| `ila` | `if` | If statement |
| `awla ila` | `elif` | Else-if statement |
| `awla` | `else` | Else statement |
| `3la` | `for` | For loop |
| `htta` | `while` | While loop |
| `hbs` | `break` | Break loop |
| `kml` | `continue` | Continue loop |

### Functions & Classes
| Darija | Python | Description |
| :--- | :--- | :--- |
| `3rf` | `def` | Define function |
| `rj3` | `return` | Return statement |
| `class` | `class` | Define class |
| `bda` | `__init__` | Constructor |
| `rassi` | `self` | Class instance (self) |

### Common Functions
| Darija | Python | Description |
| :--- | :--- | :--- |
| `weri` | `print` | Print to console |
| `dkhl` | `input` | Take user input |
| `toul` | `len` | Get length |
| `no3` | `type` | Get object type |
| `mn-l-7ta` | `range` | Range function |

---

## 🎨 Color Support

You can add color to your console output using these built-in color constants:

- `7mer`: Red
- `khder`: Green
- `sfer`: Yellow
- `zreq`: Blue
- `smawi`: Cyan
- `bold`: Bold text
- `rj3_no3`: Reset color (always use this at the end of a colored string!)

**Example:**
```python
weri(khder + "Sba7 lkhir!" + rj3_no3)
```

---

## 💡 Important Notes

### Identifiers Starting with Numbers
In Python, variable and function names **cannot** start with a number. Since Darija uses phonetic numbers (like `7ssab`, `3ref`), our interpreter automatically handles this for you:
- Any Darija token starting with a number (e.g., `7ssab`) is automatically converted to a valid Python identifier (e.g., `_7ssab`) behind the scenes.
- Pure numbers (like `0`, `10`, `3.14`) are preserved as-is.

### Keywords as Variables
Avoid naming your variables the same as keywords (e.g., don't name a variable `ila` or `smiya`) to avoid syntax errors in the generated code.

---

### Data Types
- `ra9m`: int
- `ra9m_blfasila`: float
- `klma`: str
- `s7i7_ghalat`: bool
- `lista`: list

---

## 💻 VS Code Extension

To install the syntax highlighting locally:
1.  Copy the `darijalang-extension` folder to your VS Code extensions directory (typically `%USERPROFILE%\.vscode\extensions`).
2.  Alternatively, open the folder in VS Code and press **F5** to launch the Extension Development Host.
3.  Open any file ending in `.daria` to see your code colored and themed!

---

## 🌟 Example Code (`main.daria`)

```python
3rf sba7_lkhir(klma smiya):
    weri("Sba7 lkhir, " + smiya)

smiya = dkhl("Xno smitek? ")
sba7_lkhir(smiya)

z = 30
ila z > 10:
    weri("z kbir mn 10")
awla ila z == 10:
    weri("z katsawi 10")
awla:
    weri("z sghir mn 10")

weri("L2ar9am mn 0 tal 4:")
3la i f mn-l-7ta(5):
    weri(i)
```

---

## 🤝 Contributing
Feel free to fork this project and add more keywords to `sintax.txt` or improve the grammar in the VS Code extension!

---

**Shed l-khet, bda t-coder!** 💻🇲🇦
