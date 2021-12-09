# Compiladores - Trabalho final
## Aluno: Luís Antônio da Silva Dourado - <>
Este repositório possui o código fonte do trabalho final da disciplina de Compiladores I do Instituto de Computação da UFMT.

## Instalação

Para a execução do trabalho, é necessário que haja o [Python3](https://www.python.org/downloads/) instalado na máquina.

Com o Python instalado, basta digitar o seguinte comando:

```bash
python3 main.py test.txt
```

## Autômato: Analisador Léxico

![Autômato da análise léxica](https://raw.githubusercontent.com/luisdourado33/compiladores/master/analisador-lexico.png)

## Regra semântica: Gramática

```
<programa> -> program ident <corpo> .
<corpo> -> <dc> begin <comandos> end
<dc> -> <dc_v> <mais_dc>  | λ
<mais_dc> -> ; <dc> | λ
<dc_v> ->  <tipo_var> : <variaveis>
<tipo_var> -> real | integer
<variaveis> -> ident <mais_var>
<mais_var> -> , <variaveis> | λ
<comandos> -> <comando> <mais_comandos>
<mais_comandos> -> ; <comandos> | λ

<comando> ->    read (ident) |
                write (ident) |
                ident := <expressao> |
                if <condicao> then <comandos> <pfalsa> $
							
<condicao> -> <expressao> <relacao> <expressao>
<relacao> -> = | <> | >= | <= | > | <
<expressao> -> <termo> <outros_termos>
<termo> -> <op_un> <fator> <mais_fatores>
<op_un> -> - | λ
<fator> -> ident | numero_int | numero_real | (<expressao>)
<outros_termos> -> <op_ad> <termo> <outros_termos> | λ
<op_ad> -> + | -
<mais_fatores> -> <op_mul> <fator> <mais_fatores> | λ
<op_mul> -> * | /
<pfalsa> -> else <comandos> | λ
```
