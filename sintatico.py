"""
Universidade Federal de Mato Grosso - UFMT
Luís Antônio da Silva Dourado
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
            print(self.tokenAtual.msg)
            self.tokenAtual = self.lex.getToken()
            if self.gerar_tokens:
                self.tokens.append(self.tokenAtual)
        else:
            (_, msg) = token
            print('ERRO DE SINTAXE [linha %d]: era esperado "%s" mas veio "%s"'
                  % (self.tokenAtual.linha, msg, self.tokenAtual.lexema))
            quit()

    def P(self):
        self.escopo()

    def escopo(self):
        self.consome(tt.PROGRAM)
        self.consome(tt.ID)
        self.corpo()

        self.consome(tt.PONTO)

    def corpo(self):
        # print('<corpo>')
        self.declara()

        self.consome(tt.BEGIN)
        self.comandos()
        self.consome(tt.END)

    def declara(self):
        # print('<dc>')
        if self.atualIgual(tt.REAL) or self.atualIgual(tt.INTEGER):
            self.declara_var()
            self.continua_declaracao()

    def continua_declaracao(self):
        # print('<mais_dc>')
        if self.atualIgual(tt.PVIRG):
            self.consome(tt.PVIRG)
            self.declara()

    def declara_var(self):
        # print('<dc_v>')
        self.tipo_variavel()

        self.consome(tt.DPONTOS)
        self.variaveis()

    def tipo_variavel(self):
        # print('<tipo_Var>')
        if self.atualIgual(tt.REAL):
            self.consome(tt.REAL)
        elif self.atualIgual(tt.INTEGER):
            self.consome(tt.INTEGER)

    def variaveis(self):
        # print('<variaveis>')
        self.consome(tt.ID)
        self.mais_var()

    def mais_var(self):
        # print('<mais_var>')
        if self.atualIgual(tt.VIRG):
            self.consome(tt.VIRG)
            self.variaveis()

    def comandos(self):
        # print('<comandos>')
        self.comando()
        self.mais_comandos()

    def mais_comandos(self):
        # print('<mais_comandos>')
        if self.atualIgual(tt.PVIRG):
            self.consome(tt.PVIRG)
            self.comandos()

    def comando(self):
        # print('<comando>')
        if self.atualIgual(tt.READ):
            self.consome(tt.READ)
            if self.atualIgual(tt.ABREPAR):
                self.consome(tt.ABREPAR)
                self.consome(tt.ID)
                if self.atualIgual(tt.FECHAPAR):
                    self.consome(tt.FECHAPAR)

        elif self.atualIgual(tt.WRITE):
            self.consome(tt.WRITE)

            if self.atualIgual(tt.ABREPAR):
                self.consome(tt.ABREPAR)
                self.consome(tt.ID)
                if self.atualIgual(tt.FECHAPAR):
                    self.consome(tt.FECHAPAR)

        elif self.atualIgual(tt.IF):
            self.consome(tt.IF)
            self.condicao()

            self.consome(tt.THEN)
            self.comandos()
            self.falsa_condicao()

            self.consome(tt.CIF)

        elif self.atualIgual(tt.ID):
            self.consome(tt.ID)

            self.consome(tt.ATRIB)
            self.expressao()

    def condicao(self):
        # print('<condicao>')
        self.expressao()
        self.relacao()
        self.expressao()

    def relacao(self):
        # print('<relacao>')
        if self.atualIgual(tt.IGUAL):
            self.consome(tt.IGUAL)
        if self.atualIgual(tt.DIFERENTE):
            self.consome(tt.DIFERENTE)
        if self.atualIgual(tt.MAIORIGUAL):
            self.consome(tt.MAIORIGUAL)
        if self.atualIgual(tt.MENORIGUAL):
            self.consome(tt.MENORIGUAL)
        if self.atualIgual(tt.MAIOR):
            self.consome(tt.MAIOR)
        if self.atualIgual(tt.MENOR):
            self.consome(tt.MENOR)

    def expressao(self):
        # print('<expressao>')
        self.termo()
        self.outros_termos()

    def termo(self):
        # print('<termo>')
        self.subtracao()
        self.fator()
        self.mais_fatores()

    def subtracao(self):
        # print('<op_un>')
        if self.atualIgual(tt.SUBTRACAO):
            self.consome(tt.SUBTRACAO)

    def fator(self):
        # print('<fator>')
        if self.atualIgual(tt.ID):
            self.consome(tt.ID)
        elif self.atualIgual(tt.ABREPAR):
            self.consome(tt.ABREPAR)
            self.expressao()

            if self.atualIgual(tt.FECHAPAR):
                self.consome(tt.FECHAPAR)

    def outros_termos(self):
        # print('<outros_termos>')
        if self.atualIgual(tt.SOMA) or self.atualIgual(tt.SUBTRACAO):
            self.op_ad()
            self.termo()
            self.outros_termos()

    def op_ad(self):
        # print('<op_ad>')
        if self.atualIgual(tt.SOMA):
            self.consome(tt.SOMA)

        if self.atualIgual(tt.SUBTRACAO):
            self.consome(tt.SUBTRACAO)

    def mais_fatores(self):
        # print('<mais_fatores>')
        if self.atualIgual(tt.MULTIPLICACAO) or self.atualIgual(tt.DIVISAO):
            self.op_mul()
            self.fator()
            self.mais_fatores()

    def op_mul(self):
        # print('<op_mul>')
        if self.atualIgual(tt.MULTIPLICACAO):
            self.consome(tt.MULTIPLICACAO)
        else:
            self.consome(tt.DIVISAO)

    def falsa_condicao(self):
        # print('<p_falsa>')
        self.consome(tt.ELSE)
        self.comandos()
