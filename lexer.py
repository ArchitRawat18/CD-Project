import re

# Define simple token specs for MiniC
token_specs = [
    ('KEYWORD', r'\b(int|float|if|else|while|return)\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('NUMBER', r'\b\d+(\.\d+)?\b'),
    ('OPERATOR', r'==|!=|<=|>=|[+\-*/=<>]'),
    ('SYMBOL', r'[{}();,]'),
    ('WHITESPACE', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('MISMATCH', r'.'),
]

token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specs)

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0
    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
        elif kind == 'WHITESPACE':
            continue
        elif kind == 'MISMATCH':
            tokens.append({'type': 'ERROR', 'value': value, 'line': line_num, 'column': column})
        else:
            tokens.append({'type': kind, 'value': value, 'line': line_num, 'column': column})

    return tokens
