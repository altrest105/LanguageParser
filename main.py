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
            return re.fullmatch(r"[[0-9]+[Dd]?|[0-9]+[Ee][+-]?[0-9]+|[0-9]*\.[0-9]+([Ee][+-]?[0-9]+)?", value)

    def is_kword(self, value):
        keywords = {'not', 'or', 'and', 'as', 'if', 'then', 'else', 'for', 'to', 'do', 'while', 'read', 'write', 'true', 'false'}
        return value in keywords
    
    def add(self, token_type, value):
        self.tokens.append((token_type, value))

    def lex(self):
        while self.current_char is not None:
            # Обработка начального состояния (H)
            if self.current_char.isspace():
                self.state = 'H'
                self.next()

            # Обработка идентификаторов (ID)
            elif self.is_alpha(self.current_char):
                self.state = 'ID'
                identifier = ''
                while (self.current_char is not None) and (self.is_alphadigit(self.current_char)):
                    identifier += self.current_char
                    self.next()
                if self.is_kword(identifier):
                    self.add('KEYWORD', identifier)
                else:
                    self.add('IDENTIFIER', identifier)
                self.state = 'H'
            
            # Обработка чисел (NUM)
            elif (self.is_digit(self.current_char)) or (self.current_char == '.'):
                self.state = 'NUM'
                number = ''
                while (self.current_char is not None) and (self.is_numchar(self.current_char)):
                    number += self.current_char
                    self.next()
                if self.is_num(number):
                    self.add('NUMBER', number)
                else:
                    self.add('ERR', number)
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
                            else:
                                self.state = 'COM2'
                            
                        self.next()
                    else:
                        print('ERROR! An unclosed comment was found') # ОШИБКА! незакрытый комментарий
                
                else:
                    self.add('DELIMITER', '/')
                    self.state = 'H'
            
            # Обработка знака меньше (EQ1)
            elif self.current_char == '<':
                self.state = 'EQ1'
                delim = self.current_char
                self.next()
                if (self.current_char == '>') or (self.current_char == '='):
                    delim += self.current_char
                    self.state = 'EQ'
                    self.next()
                self.add('DELIMITER', delim)
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
                self.add('DELIMITER', delim)
                self.state = 'H'

            # Обработка знака равно (EQ)
            elif self.current_char == '=':
                self.state = 'EQ'
                self.add('DELIMITER', self.current_char)
                self.next()
                self.state = 'H'

            # Обработка операций +, -, * (OP)
            elif (self.current_char == '+') or (self.current_char == '-') or (self.current_char == '*'):
                self.state = 'OP'
                self.add('DELIMITER', self.current_char)
                self.next()
                self.state = 'H'

            # Обработка типов (TYPE)
            elif (self.current_char == '%') or (self.current_char == '!') or (self.current_char == '$'):
                self.state = 'OP'
                self.add('DELIMITER', self.current_char)
                self.next()
                self.state = 'H'
            
            # Обработка неизвестных символов
            else:
                self.state = 'ERR'
                self.add('ERR', self.current_char)
                print(f'ERROR! An unexpected symbol: {self.current_char}') # ОШИБКА Встречен неизвестный символ
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