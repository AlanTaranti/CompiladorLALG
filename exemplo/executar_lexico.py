# Exemplo de Execução do Analisador Léxico
#
# Desenvolvedor: Alan Taranti

# Main
if __name__ == "__main__":

    #
    # Importar Analisador
    #

    import sys, os

    sys.path.append("..")

    from analisador import Lexico

    dir = os.path.dirname(os.path.abspath(__file__))
    dirpath = '/'.join((dir).split('/')[:-1])+'/analisador'
    sys.path.append(dirpath)


    #
    # Ler o Arquivo
    #

    filename = 'file.lalg'
    with open(dir+'/'+filename) as f:
        alg = f.read()

    #
    # Inicializar o Analisador
    #

    lex = Lexico(alg)

    #
    # Executar
    #

    # Extrair o proximo token
    item = lex.get_next_token()

    # Enquanto não acabar os tokens, imprimí-los
    while item['token'] is not None:

        if item['tipo'] is not None:
            # Imprimir dados do token
            print('Token:',item['token'],'\t\t','ID',item['tipo'])
        else:
            # Imprimir mensagem de erro
            print('Erro: Token', item['token'], 'não reconhecido na linha:', item['linha'])

        # Extrair o proximo token
        item = lex.get_next_token()

