import re

# ==========================================
# TOKEN DEFINITIONS
# ==========================================

KEYWORDS = KEYWORDS = {'int', 'if', 'else', 'while', 'print'}

TOKEN_SPECIFICATION = [
    ('NUMBER',      r'\d+'),
    ('ID',          r'[A-Za-z_][A-Za-z0-9_]*'),
    ('REL_OP',      r'<=|>=|==|!=|<|>'),
    ('ASSIGN',      r'='),
    ('OP',          r'[+\-*/]'),
    ('LPAREN',      r'\('),
    ('RPAREN',      r'\)'),
    ('LBRACE',      r'\{'),
    ('RBRACE',      r'\}'),
    ('SEMICOLON',   r';'),
    ('SKIP',        r'[ \t\n]+'),
    ('MISMATCH',    r'.'),
]

TOK_REGEX = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)

# ==========================================
# TOKEN CLASS
# ==========================================

class Token:

    def __init__(self, type_, value):

        self.type = type_
        self.value = value

    def __repr__(self):

        return f'({self.type}, {self.value})'

# ==========================================
# LEXER
# ==========================================

def lexer(code):

    tokens = []

    for mo in re.finditer(TOK_REGEX, code):

        kind = mo.lastgroup
        value = mo.group()

        if kind == 'ID' and value in KEYWORDS:
            kind = value.upper()

        elif kind == 'SKIP':
            continue

        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')

        tokens.append(Token(kind, value))

    return tokens

# ==========================================
# GLOBALS
# ==========================================

symbol_table = {}
ir_code = []
label_count = 0

# ==========================================
# LABEL GENERATOR
# ==========================================

def new_label():

    global label_count

    label = f"L{label_count}"
    label_count += 1

    return label

# ==========================================
# PARSER + SEMANTIC ANALYZER
# ==========================================

class Parser:

    def __init__(self, tokens):

        self.tokens = tokens
        self.pos = 0

    def current_token(self):

        if self.pos < len(self.tokens):
            return self.tokens[self.pos]

        return None

    def eat(self, token_type):

        token = self.current_token()

        if token and token.type == token_type:
            self.pos += 1

        else:
            raise SyntaxError(
                f"Expected {token_type}, got {token.type if token else 'EOF'}"
            )

    # ======================================
    # PROGRAM
    # ======================================

    def parse(self):

        while self.current_token() is not None:
            self.statement()

    # ======================================
    # STATEMENTS
    # ======================================

    def statement(self):

        token = self.current_token()

        if token.type == 'INT':
            self.declaration()

        elif token.type == 'ID':
            self.assignment()

        elif token.type == 'IF':
            self.if_statement()

        elif token.type == 'WHILE':
            self.while_statement()

        elif token.type == 'PRINT':
            self.print_statement()

        else:
            raise SyntaxError(f"Invalid statement near {token.value}")

    # ======================================
    # DECLARATION
    # ======================================

    def declaration(self):

        self.eat('INT')

        var_name = self.current_token().value

        if var_name in symbol_table:
            raise Exception(f"Semantic Error: '{var_name}' already declared")

        symbol_table[var_name] = 'int'

        self.eat('ID')
        self.eat('SEMICOLON')

    # ======================================
    # ASSIGNMENT
    # ======================================

    def assignment(self):

        var_name = self.current_token().value

        if var_name not in symbol_table:
            raise Exception(f"Semantic Error: '{var_name}' not declared")

        self.eat('ID')
        self.eat('ASSIGN')

        self.expression()

        ir_code.append(f"STORE {var_name}")

        self.eat('SEMICOLON')

    # ======================================
    # EXPRESSIONS
    # ======================================

    def expression(self):

        self.term()

        while self.current_token() and self.current_token().type == 'OP':

            op = self.current_token().value

            self.eat('OP')

            self.term()

            if op == '+':
                ir_code.append("ADD")

            elif op == '-':
                ir_code.append("SUB")

            elif op == '*':
                ir_code.append("MUL")

            elif op == '/':
                ir_code.append("DIV")

    def term(self):

        token = self.current_token()

        if token.type == 'NUMBER':

            ir_code.append(f"PUSH {token.value}")
            self.eat('NUMBER')

        elif token.type == 'ID':

            if token.value not in symbol_table:
                raise Exception(
                    f"Semantic Error: '{token.value}' not declared"
                )

            ir_code.append(f"LOAD {token.value}")
            self.eat('ID')

        else:
            raise SyntaxError("Invalid expression")

    # ======================================
    # CONDITION
    # ======================================

    def condition(self):

        self.expression()

        op = self.current_token().value

        self.eat('REL_OP')

        self.expression()

        ir_code.append(f"COMPARE {op}")

    # ======================================
    # IF ELSE
    # ======================================

    def if_statement(self):

        self.eat('IF')
        self.eat('LPAREN')

        self.condition()

        self.eat('RPAREN')

        false_label = new_label()
        end_label = new_label()

        ir_code.append(f"JZ {false_label}")

        self.eat('LBRACE')

        while self.current_token().type != 'RBRACE':
            self.statement()

        self.eat('RBRACE')

        ir_code.append(f"JMP {end_label}")
        ir_code.append(f"LABEL {false_label}")

        if self.current_token() and self.current_token().type == 'ELSE':

            self.eat('ELSE')
            self.eat('LBRACE')

            while self.current_token().type != 'RBRACE':
                self.statement()

            self.eat('RBRACE')

        ir_code.append(f"LABEL {end_label}")

    # ======================================
    # WHILE LOOP
    # ======================================

    def while_statement(self):

        start_label = new_label()
        end_label = new_label()

        ir_code.append(f"LABEL {start_label}")

        self.eat('WHILE')
        self.eat('LPAREN')

        self.condition()

        self.eat('RPAREN')

        ir_code.append(f"JZ {end_label}")

        self.eat('LBRACE')

        while self.current_token().type != 'RBRACE':
            self.statement()

        self.eat('RBRACE')

        ir_code.append(f"JMP {start_label}")
        ir_code.append(f"LABEL {end_label}")

    # ======================================
    # PRINT
    # ======================================

    def print_statement(self):

        self.eat('PRINT')
        self.eat('LPAREN')

        self.expression()

        ir_code.append("PRINT")

        self.eat('RPAREN')
        self.eat('SEMICOLON')

# ==========================================
# INPUT METHOD SELECTION
# ==========================================

print("===================================")
print(" MINI COMPILER ")
print("===================================")

print("\nSelect Input Method:")
print("1. Upload source code file")
print("2. Enter source code manually")

choice = input("\nEnter your choice (1 or 2): ")

# ==========================================
# OPTION 1 → FILE UPLOAD
# ==========================================

if choice == '1':

    print("\nEnter the full path to your source code file (.txt):")

    filename = input().strip().strip('"')

    with open(filename, 'r', encoding='utf-8') as file:
        source_code = file.read()

# ==========================================
# OPTION 2 → MANUAL INPUT
# ==========================================

elif choice == '2':

    print("\nEnter your source code below.")
    print("Type END on a new line to finish:\n")

    lines = []

    while True:

        line = input()

        if line == "END":
            break

        lines.append(line)

    source_code = "\n".join(lines)

# ==========================================
# INVALID OPTION
# ==========================================

else:

    print("\nInvalid choice!")
    exit()

# ==========================================
# MAIN DRIVER
# ==========================================

try:

    print("\n========== SOURCE CODE ==========\n")
    print(source_code)

    # LEXICAL ANALYSIS
    tokens = lexer(source_code)

    print("\n========== TOKENS ==========\n")

    for token in tokens:
        print(token)

    # PARSING + SEMANTIC ANALYSIS
    parser = Parser(tokens)
    parser.parse()

    # SYMBOL TABLE
    print("\n========== SYMBOL TABLE ==========\n")

    for var, typ in symbol_table.items():
        print(f"{var} --> {typ}")

    # IR CODE
    print("\n========== INTERMEDIATE CODE ==========\n")

    for line in ir_code:
        print(line)

    print("\nCompilation Successful!")

except Exception as e:

    print("\nERROR:", e)

