# Exemplo de Execução do Analisador Sintático
#
# Desenvolvedor: Alan Taranti

# Main
if __name__ == "__main__":

    #
    # Importar Analisador
    #

    import sys, os

    sys.path.append("..")

    from analisador import Sintatico

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

    sin = Sintatico(alg)

    #
    # Executar
    #

    print('\nAnálise Lexica e Sintática:\n')
    resultado = sin.start()

    print('\n' + resultado['mensagem'])

