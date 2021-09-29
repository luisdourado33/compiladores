"""
Universidade Federal de Mato Grosso - UFMT

Aluno: Luis Antonio da Silva Dourado
RGA: 201621901003
<luis_dourado33@hotmail.com>

"""

from sintatico import Sintatico
from sys import argv

if __name__== "__main__":

    nome = argv[1]
    parser = Sintatico(True)
    parser.interprete(nome)

    for i in range(len(argv)):
        if (argv[i] == '-t'):
            arquivo = open(argv[i+1], 'wt')
            tokens = []
            for token in parser.tokens:
                print(token)
                tokens.append(token.msg)
            arquivo.write(str(tokens))
