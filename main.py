import re

class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.current_char = self.input[self.position]
        self.tokens = []
        self.state = 'H'

    def next(self):
        self.position += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None
    
    def is_alphadig(self, value):
        return re.match(r"[a-zA-Z0-9]", value)

    def is_alphanum(self, value):
            return re.match(r"[a-zA-Z0-9+-.]", value)
    
    def is_alpha(self, value):
        return re.match(r"[a-zA-Z]", value)

    def is_digit(self, value):
        return re.match(r"[0-9]", value)
    
    def is_num(self, value):
        return re.match(r"[01]+[bB]|[0-7]+[oO]|[0-9]+[dD]|[0-9][0-9a-fA-F]*[hH]|[0-9]+[eE][+-]?[0-9]+|[0-9]*\.[0-9]+([eE][+-]?[0-9]+)?", value)

    def is_kword(self, value):
        keywords = {'not', 'or', 'and', 'as', 'if', 'then', 'else', 'for', 'to', 'do', 'while', 'read', 'write', 'true', 'false'}
        return value in keywords
    
    def add(self, token_type, value):
        self.tokens.append((token_type, value))

    def lex(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.state = 'H'
                self.next()

            elif self.current_char in '<>=+-*/%!$':
                delim = self.current_char
                if delim in ('+-*/%!$'):
                    self.add('DELIM', self.current_char)
                    self.next()
                else:
                    self.next()
                    delim += self.current_char
                    self.next()
                    if delim in ('<>', '>=', '<='):
                        self.add('DELIM', delim)
                    elif delim[0] == '=':
                        self.add('DELIM', '=')
                    else:
                        self.add('ERR', delim)
                    self.next()
                self.state = 'H'

            elif self.is_alpha(self.current_char):
                self.state = 'ID'
                identifier = ''
                while self.current_char is not None and self.is_alphadig(self.current_char):
                    identifier += self.current_char
                    self.next()
                if self.is_kword(identifier):
                    self.add('KEYWORD', identifier)
                else:
                    self.add('ID', identifier)
                self.state = 'H'

            elif self.is_digit(self.current_char) or self.current_char == '.':
                self.state = 'NM'
                number = self.current_char
                self.next()
                while self.current_char is not None and self.is_digit(self.current_char):
                    number += self.current_char
                    self.next()

                if self.is_alphanum(self.current_char):
                    number += self.current_char
                    self.next()
                    while self.current_char is not None and self.is_alphanum(self.current_char):
                        number += self.current_char
                        self.next()

                if self.is_num(number):
                    self.state = 'H'
                    self.add('NUMBER', number)
                else:
                    self.state = 'ERR'
                    self.add('ERR', number)

            else:
                self.state = 'ERR'
                self.add('ERR', self.current_char)
                self.next()

        return self.tokens


if __name__ == '__main__':
    with open('input.txt') as file:
        code = file.read()
    lexer = Lexer(code)
    tokens = lexer.lex()
    for token in tokens:
        print(token)