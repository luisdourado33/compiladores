"""
Universidade Federal de Mato Grosso - UFMT

Aluno: Luis Antonio da Silva Dourado
RGA: 201621901003
<luis_dourado33@hotmail.com>

"""
from os import path


class TipoToken:
    # tipos de tokens
    ID = (1, 'ID')
    CTE = (2, 'NUM')
    STR = (3, 'STR')
    ATRIB = (4, ':=')
    OPAD = (5, 'OPAD')
    PVIRG = (6, ';')
    DPONTOS = (7, ':')
    VIRG = (8, ',')
    # palavras reservadas
    VAR = (9, 'VAR')
    INTEGER = (10, 'INTEGER')
    REAL = (11, 'REAL')
    IF = (12, 'IF')
    THEN = (13, 'THEN')
    PROGRAM = (14, 'PROGRAM')
    # erro token, nao esta presente gramatica
    ERROR = (15, 'ERRO')
    EOF = (16, 'EOF')
    BEGIN = (17, 'BEGIN')
    END = (18, 'END')
    READ = (19, 'READ')
    FECHAPAR = (20, "" + ")" + "")
    ABREPAR = (21, "" + "(" + "")
    CIF = (22, '$')
    DIFERENTE = (23, '<>')
    MAIORIGUAL = (24, '>=')
    MENORIGUAL = (25, '<=')
    MAIOR = (26, '>')
    MENOR = (27, '<')
    IGUAL = (28, '=')
    SUBTRACAO = (29, '-')
    SOMA = (30, '+')
    MULTIPLICACAO = (31, '*')
    DIVISAO = (32, '/')
    ELSE = (33, 'ELSE')
    WRITE = (34, 'WRITE')
    PONTO = (35, '.')


class Token:
    def __init__(self, tipo, lexema, linha):
        self.tipo = tipo
        (const, msg) = tipo
        self.const = const
        self.msg = msg
        self.lexema = lexema
        self.linha = linha


class Lexico:
    # dicionario palavras-reservadas
    reservadas = {
        'PROGRAM': TipoToken.PROGRAM,
        'VAR': TipoToken.VAR,
        'INTEGER': TipoToken.INTEGER,
        'REAL': TipoToken.REAL,
        'IF': TipoToken.IF,
        'ELSE': TipoToken.ELSE,
        'THEN': TipoToken.THEN,
        'BEGIN': TipoToken.BEGIN,
        'END': TipoToken.END,
        'READ': TipoToken.READ,
        'WRITE': TipoToken.WRITE,
        '(': TipoToken.ABREPAR,
        ')': TipoToken.FECHAPAR,
        '$': TipoToken.CIF,
        '.': TipoToken.PONTO,
        'MULTIPLICACAO': TipoToken.MULTIPLICACAO,
    }

    def __init__(self, nomeArquivo):
        self.nomeArquivo = nomeArquivo
        self.arquivo = None
        # os atributos buffer e linha sao incluidos no metodo abreArquivo

    # abre arquivo caso nao esteja aberto (se existir)
    def abreArquivo(self):
        if not self.arquivo is None:
            print('ERRO: Arquivo ja aberto')
            quit()
        elif path.exists(self.nomeArquivo):
            self.arquivo = open(self.nomeArquivo, "r")
            # file de carac desalocados pelo ungetChar
            self.buffer = ''
            self.linha = 1
        else:
            print('ERRO: Arquivo "%s" inexistente.' % self.nomeArquivo)
            quit()

    def fechaArquivo(self):
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        else:
            self.arquivo.close()

    def getChar(self) -> str:
        if self.arquivo is None:
            print('ERRO: Nao ha arquivo aberto')
            quit()
        elif len(self.buffer) > 0:
            c = self.buffer[0]
            self.buffer = self.buffer[1:]
            print(c.lower())
            return c.lower()
        else:
            c = ''
            try:
                c = self.arquivo.read(1)
            except UnicodeDecodeError:
                pass

            # se nao foi eof, pelo menos um car foi lido
            # senao len(c) == 0
            if len(c) == 0:
                return None
            else:
                return c.lower()

    def ungetChar(self, c: str):
        if not c is None:
            self.buffer = self.buffer + c

    def getToken(self):
        estado = 1
        car = None
        lexema = ''
        while (True):
            if estado == 1:
                # estado inicial que faz primeira classificacao
                car = self.getChar()
                if car is None:
                    return Token(TipoToken.EOF, '<eof>', self.linha)
                elif car in {' ', '\t', '\n'}:
                    if car == '\n':
                        self.linha += 1
                elif car.isalpha():
                    estado = 2
                elif car.isdigit():
                    estado = 2
                elif car in {':', '=', '<', '>', ',', ';', '+', '-', '*', '(', ')', '{', '}', '$', '.'}:
                    estado = 3
                elif car == '/':
                    lexema = car
                    lexema += self.getChar()
                    if (lexema == '//' or lexema == '/*'):
                        estado = 4
                    else:
                        self.ungetChar(lexema[1:])
                        lexema = ''
                        estado = 3
                else:
                    return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 2:
                # estado que trata nomes (identificadores ou palavras reservadas)
                lexema = car
                while(car != None and car.isalnum()):
                    car = self.getChar()
                    if(car != None):
                        lexema += car
                if (car is None) or (not car.isalnum()):
                    # terminou o nome
                    if not len(lexema) == 1:
                        self.ungetChar(car)
                        lexema = lexema[:-1].strip()
                    if lexema.upper() in Lexico.reservadas:
                        return Token(Lexico.reservadas[lexema.upper()], lexema, self.linha)
                    else:
                        return Token(TipoToken.ID, lexema, self.linha)
            elif estado == 3:
                # estado que trata outros tokens primitivos comuns
                if car == ':':
                    lexema = car
                    lexema += self.getChar()
                    if lexema == ':=':
                        return Token(TipoToken.ATRIB, lexema, self.linha)
                    else:
                        self.ungetChar(lexema[-1])
                        
                        return Token(TipoToken.DPONTOS, car, self.linha)
                elif car == ';':
                    return Token(TipoToken.PVIRG, car, self.linha)
                elif car == ',':
                    return Token(TipoToken.VIRG, car, self.linha)
                elif car == '+':
                    return Token(TipoToken.SOMA, car, self.linha)
                elif car == '>':
                    return Token(TipoToken.MAIOR, car, self.linha)
                elif car == '<':
                    return Token(TipoToken.MENOR, car, self.linha)
                elif car == '>=':
                    return Token(TipoToken.MAIORIGUAL, car, self.linha)
                elif car == '<=':
                    return Token(TipoToken.MENORIGUAL, car, self.linha)
                elif car == '(':
                    return Token(TipoToken.ABREPAR, car, self.linha)
                elif car == '*':
                    return Token(TipoToken.MULTIPLICACAO, car, self.linha)
                elif car == '$':
                    return Token(TipoToken.CIF, car, self.linha)
                elif car == ')':
                    return Token(TipoToken.FECHAPAR, car, self.linha)
                elif car == '.':
                    return Token(TipoToken.PONTO, car, self.linha)
                return Token(TipoToken.ERROR, '<' + car + '>', self.linha)
            elif estado == 4:
                # consumindo comentario
                if lexema == '//':
                    while (not car is None) and (car != '\n'):
                        car = self.getChar()
                    estado = 1
                elif lexema == '/*':
                    while (estado != 1):
                        car = self.getChar()
                        if (car is None):
                            estado = 1
                            continue
                        if (car == '*'):
                            car = self.getChar()
                            if (car == '/'):
                                estado = 1
                                continue
