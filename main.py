import re

groups = {
    # Ошибка
    0: 'ERROR',

    # Идентификаторы
    1: 'IDENTIFIER',

    # Числа
    2: 'NUMBER',

    # Ключевые слова
    3: 'LEX_NOT',
    4: 'LEX_OR',
    5: 'LEX_AND',
    6: 'LEX_AS',
    7: 'LEX_IF',
    8: 'LEX_THEN',
    9: 'LEX_ELSE',
    10: 'LEX_FOR',
    11: 'LEX_TO',
    12: 'LEX_DO',
    13: 'LEX_WHILE',
    14: 'LEX_READ',
    15: 'LEX_WRITE',
    16: 'LEX_TRUE',
    17: 'LEX_FALSE',
    
    # Разделители
    18: 'LEX_SLASH',
    19: 'LEX_PLUS',
    20: 'LEX_MINUS',
    21: 'LEX_ASTERISK',
    22: 'LEX_NOT_EQUAL',
    23: 'LEX_EQUALS',
    24: 'LEX_LESS_THAN',
    25: 'LEX_LESS_EQUAL',
    26: 'LEX_GREATER_THAN',
    27: 'LEX_GREATER_EQUAL',
    28: 'LEX_PERCENT',
    29: 'LEX_EXCLAMATION',
    30: 'LEX_DOLLAR',
    31: 'LEX_LEFT_PAREN',
    32: 'LEX_RIGHT_PAREN',
    33: 'LEX_LEFT_BRACKET',
    34: 'LEX_RIGHT_BRACKET',
    35: 'LEX_LEFT_BRACE',
    36: 'LEX_RIGHT_BRACE',
    37: 'LEX_SEMICOLON',
    38: 'LEX_COLON',
    39: 'LEX_COMMA',
}

lexems = {
    'IDENTIFIER': 1,
    'NUMBER': 2,
    'not': 3,
    'or': 4,
    'and': 5,
    'as': 6,
    'if': 7,
    'then' : 8,
    'else': 9,
    'for': 10,
    'to': 11,
    'do': 12,
    'while': 13,
    'read': 14,
    'write': 15,
    'true': 16,
    'false': 17,
    '/': 18,
    '+': 19,
    '-': 20,
    '*': 21,
    '<>': 22,
    '=': 23,
    '<': 24,
    '<=': 25,
    '>': 26,
    '>=': 27,
    '%': 28,
    '!': 29,
    '$': 30,
    '(': 31,
    ')': 32,
    '[': 33,
    ']': 34,
    '{': 35,
    '}': 36,
    ';': 37,
    ':': 38,
    ',': 39,
}

def error_message(message, index, line):
    print(f'[ERROR] {message} at line {line}, position {index}')
    exit(1)

class Lexer:
    def __init__(self, input):
        self.input = input
        self.position = 0
        self.current_char = self.input[self.position]
        self.tokens = []
        self.state = 'H'
        self.x = 1
        self.y = 1

    def next(self):
        self.position += 1
        self.x += 1
        if self.position < len(self.input):
            self.current_char = self.input[self.position]
        else:
            self.current_char = None
    
    def is_alpha(self, value):
        return re.match(r"[a-zA-Z]", value)

    def is_digit(self, value):
        return re.match(r"[0-9]", value)
    
    def is_alphadigit(self, value):
        return re.match(r"[a-zA-Z0-9]", value)
    
    def is_numchar(self, value):
        return re.match(r"[a-zA-Z0-9+-.]", value)
    
    def is_num(self, value):
        if (value[-1] == 'B') or (value[-1] == 'b'):
            return re.fullmatch(r"[01]+[Bb]", value)
        elif (value[-1] == 'O') or (value[-1] == 'o'):
            return re.fullmatch(r"[0-7]+[Oo]", value)
        elif (value[-1] == 'H') or (value[-1] == 'h'):
            return re.fullmatch(r"[0-9][0-9a-fA-F]*[Hh]", value)
        else:
            return re.fullmatch(r"[0-9]+[Dd]?|[0-9]+[Ee][+-]?[0-9]+|[0-9]*\.[0-9]+([Ee][+-]?[0-9]+)?", value)

    def is_kword(self, value):
        keywords = {'not', 'or', 'and', 'as', 'if', 'then', 'else', 'for', 'to', 'do', 'while', 'read', 'write', 'true', 'false'}
        return value in keywords
    
    def add(self, group_number, value):
        self.tokens.append((group_number, value, self.x-len(value), self.y))

    def lex(self):
        while self.current_char is not None:
            # Обработка начального состояния (H)
            if self.current_char.isspace():
                self.state = 'H'
                if self.current_char == '\n':
                    self.x = 1
                    self.y += 1
                self.next()

            # Обработка идентификаторов (ID)
            elif self.is_alpha(self.current_char):
                self.state = 'ID'
                identifier = ''
                while (self.current_char is not None) and (self.is_alphadigit(self.current_char)):
                    identifier += self.current_char
                    self.next()
                if self.is_kword(identifier):
                    self.add(lexems[identifier], identifier)
                else:
                    self.add(lexems['IDENTIFIER'], identifier)
                self.state = 'H'
            
            # Обработка чисел (NUM)
            elif (self.is_digit(self.current_char)) or (self.current_char == '.'):
                self.state = 'NUM'
                number = ''
                while (self.current_char is not None) and (self.is_numchar(self.current_char)):
                    number += self.current_char
                    self.next()
                if self.is_num(number):
                    self.add(lexems['NUMBER'], number)
                else:
                    self.add(0, number)
                    error_message(f'An unexpected number "{number}" was encountered', self.x, self.y)
                self.state = 'H'
            
            # Обработка комментариев и деления (OP+COM2+COM3)
            elif self.current_char == '/':
                self.state = 'OP'
                self.next()

                if self.current_char == '*':
                    self.state = 'COM2'
                    self.next()
                    while (self.current_char is not None) and (self.state == 'COM2'):

                        if self.current_char == '*':
                            self.state = 'COM3'
                            self.next()

                            if self.current_char == '/':
                                self.state = 'H'
                                self.next()
                                break
                            else:
                                self.state = 'COM2'
                            
                        self.next()
                    else:
                        error_message('An unclosed comment was found', self.x, self.y)
                
                else:
                    self.add(lexems['/'], '/')
                    self.state = 'H'
            
            # Обработка знака меньше (EQ1)
            elif self.current_char == '<':
                self.state = 'EQ1'
                delim = self.current_char
                self.next()
                if self.current_char in {'>', '='}:
                    delim += self.current_char
                    self.state = 'EQ'
                    self.next()
                self.add(lexems[delim], delim)
                self.state = 'H'

            # Обработка знака больше (EQ2)
            elif self.current_char == '>':
                self.state = 'EQ2'
                delim = self.current_char
                self.next()
                if self.current_char == '=':
                    delim += self.current_char
                    self.state = 'EQ'
                    self.next()
                self.add(lexems[delim], delim)
                self.state = 'H'

            # Обработка знака равно (EQ)
            elif self.current_char == '=':
                self.state = 'EQ'
                self.add(lexems[delim], self.current_char)
                self.next()
                self.state = 'H'

            # Обработка операций +, -, * (OP)
            elif self.current_char in {'+', '-', '*'}:
                self.state = 'OP'
                self.add(lexems[delim], self.current_char)
                self.next()
                self.state = 'H'

            # Обработка типов (TYPE)
            elif self.current_char in {'%', '!', '$'}:
                self.state = 'OP'
                self.add(lexems[delim], self.current_char)
                self.next()
                self.state = 'H'

            # Обработка скобок (DELIM)
            elif self.current_char in {'(', ')', '[', ']', '{', '}', ';', ':', ','}:
                self.state = 'DELIM'
                self.add(lexems[delim], self.current_char)
                self.next()
                self.state = 'H'
            
            # Обработка неизвестных символов
            else:
                self.state = 'ERR'
                self.add(0, self.current_char)
                error_message(f'An unexpected symbol {self.current_char}', self.x, self.y)
                self.next()
                self.state = 'H'

        return self.tokens


if __name__ == '__main__':
    with open('input.txt') as file:
        code = file.read()
    lexer = Lexer(code)
    tokens = lexer.lex()
    for token in tokens:
        print(token)