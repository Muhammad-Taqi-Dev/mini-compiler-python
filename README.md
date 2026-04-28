# Mini Compiler in Python

This repository contains a small educational compiler written in Python. It reads a tiny C-like language, tokenizes it, parses it, performs simple semantic checks, and emits intermediate code.

The project is intentionally compact so it can be used to study the basic stages of a compiler pipeline:

1. Lexical analysis
2. Syntax parsing
3. Semantic validation
4. Intermediate code generation

The main script is [CD Project.py](CD%20Project.py).

## What It Does

The compiler supports:

- integer declarations with `int`
- assignments
- arithmetic expressions with `+`, `-`, `*`, and `/`
- relational operators with `>`, `<`, `>=`, `<=`, `==`, and `!=`
- `if` / `else` statements
- `while` loops
- `print(...)` statements
- a symbol table for declared variables
- stack-style intermediate representation output

## Project Structure

- [CD Project.py](CD%20Project.py) - main compiler implementation
- [Input 1.txt](Input%201.txt) - sample source program
- [input 2.txt](input%202.txt) - sample source program
- [input 3.txt](input%203.txt) - sample source program

## Quick Start

### Requirements

- Python 3
- Windows PowerShell or Command Prompt

### Run the compiler

Open a terminal in this folder and run:

```powershell
python "CD Project.py"
```

When the script starts, it asks how you want to provide the source code.

### Option 1: Read from a file

Choose `1`, then enter the full path to a `.txt` file.

Example:

```text
1
D:\NED\CD\CD PROJECT\Input 1.txt
```

### Option 2: Type source code manually

Choose `2`, enter the source code line by line, and finish with `END` on a new line.

Example:

```text
2
int a;
a = 1;
print(a);
END
```

## Example Program

```c
int a;
int b;
int sum;

a = 15;
b = 5;
sum = a + b;

if (sum > 10)
{
    print(sum);
}
else
{
    print(a);
}

while (a > 0)
{
    print(a);
    a = a - 1;
}
```

## Output Example

For valid input, the script prints:

- the original source code
- the token list
- the symbol table
- the generated intermediate code
- a final success message

Example intermediate instructions:

```text
PUSH 1
STORE a
LOAD a
PRINT
```

## Language Rules

The accepted syntax is intentionally small.

| Construct    | Example                           |
| ------------ | --------------------------------- |
| Declaration  | `int x;`                          |
| Assignment   | `x = 10;`                         |
| Print        | `print(x);`                       |
| If statement | `if (x > 0) { ... } else { ... }` |
| While loop   | `while (x > 0) { ... }`           |

Expressions are parsed in a simple left-to-right way, which is enough for demonstration purposes but does not implement full operator precedence.

## Semantic Checks

The script enforces a few basic rules:

- variables must be declared before use
- variables cannot be declared twice
- conditions must use a relational operator

If one of these rules is broken, the program prints an error message instead of generating code.

## Troubleshooting

### `ModuleNotFoundError: No module named 'google'`

This script was originally exported from Google Colab. It no longer depends on `google.colab`, so it should run directly with Python on Windows.

### File path issues

If you choose file input, make sure the path is correct. If the path contains spaces, include it exactly as shown.

### Syntax errors

Check that:

- every declaration ends with `;`
- every assignment ends with `;`
- braces `{}` are balanced
- variables are declared before use
- conditions include a relational operator

## Notes

This is an educational compiler project, not a full programming language implementation. Its goal is to demonstrate the basic compiler workflow in a short, readable Python script.
