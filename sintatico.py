"""
Universidade Federal de Mato Grosso - UFMT

Aluno: Luís Antônio da Silva Dourado
<luis_dourado33@hotmail.com>

"""

from lexico import TipoToken as tt, Token, Lexico

class Sintatico:

    def __init__(self, gerar_tokens: bool):
        self.lex = None
        self.tokenAtual = None
        self.gerar_tokens = gerar_tokens
        self.tokens = []
    
    def interprete(self, nomeArquivo):
        if not self.lex is None:
            print('ERRO: Ja existe um arquivo sendo processado.')
        else:
            self.lex = Lexico(nomeArquivo)
            self.lex.abreArquivo()
            self.tokenAtual = self.lex.getToken()
            
            if self.gerar_tokens:
                self.tokens.append(self.tokenAtual)

            self.P()

            self.lex.fechaArquivo()

    def atualIgual(self, token):
        (const, _) = token
        return self.tokenAtual.const == const
    
    def consome(self, token):
        if self.atualIgual(token):
            self.tokenAtual = self.lex.getToken()
            if self.gerar_tokens:
                self.tokens.append(self.tokenAtual)
        else:
            (_, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
               % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def P(self):
        self.Z()
        self.consome(tt.EOF)
    
    def Z(self):
        self.I()
        self.S()
    
    def I(self):
        self.consome(tt.PROGRAM)
        self.D()
    
    def D(self):
        self.L()
        self.consome(tt.REAL)
        self.K()
        self.O()
    
    def L(self):
        self.consome(tt.ID)
        self.X()
    
    def X(self):
        if not self.atualIgual(tt.VIRG):
            pass
        else:
            self.consome(tt.VIRG)
            self.L()
    
    def K(self):
        if self.atualIgual(tt.INTEGER):
            self.consome(tt.INTEGER)
        elif self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
    
    def O(self):
        if not self.atualIgual(tt.PVIRG):
            pass
        else:
            self.consome(tt.PVIRG)
            self.D()
    
    def S(self):
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
            self.consome(tt.ATRIB)
            self.E()
        elif self.atualIgual(tt.IF):
            self.consome(tt.IF)
            self.E()
            self.consome(tt.THEN)
            self.S()
    
    def E(self):
        self.T()
        self.R()
    
    def R(self):
        if not self.atualIgual(tt.OPAD):
            pass
        else:
            self.consome(tt.OPAD)
            self.T()
            self.R()
    
    def T(self):
        self.consome(tt.ID)