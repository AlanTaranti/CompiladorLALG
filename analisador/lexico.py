#
# Analisador Léxico
#
# Desenvolvedor: Alan Taranti
#

class Lexico():
    
    def __init__(self,string):
        
        import pandas as pd

        import os

        import re
        
        # Armazena a string
        self.string = string
        
        # Controle do index
        self.index = 0

        # Controle de linha
        self.linha = 1
        
        # Tabela estados
        dir = os.path.dirname(os.path.abspath(__file__))
        filepath = dir+'/tabela_estados.csv'
        self.tabela_estados = pd.read_csv(filepath)
        
        # Palavras reservadas
        self.palavras_reservadas = [
            'program',
            'var',
            'real',
            'integer',
            'procedure',
            'begin',
            'end',
            'read',
            'write',
            'if',
            'else',
            'while',
            'then',
        ]

        # Remover comentarios
        p = re.compile("\{[\w, ]+\}")
        self.string = p.sub('', self.string)

        # Tamanho
        self.tam = len(self.string)
        
    # Verifica se o caracter eh reconhecido
    def caracter_reconhecido(self,item):

        if item not in self.tabela_estados.columns:
            print('Erro: Caracter',item,'não reconhecido')
            return False
        else:
            return True
        
    # Retorna o proximo token
    def get_next_token(self):
        
        # Ignora os FutureWarning do Pandas
        import warnings
        warnings.simplefilter(action='ignore', category=FutureWarning)
        
        # Inicializa o buffer e o estado
        buffer = ''
        estado = 0
        
        while self.index < self.tam:
            
            # Extrai o caracter
            item = self.string[self.index]
            
            # Armazena o caracter
            buffer += item

            # Transforma a string para lidar com os \n \t e etc...
            item = ('%r'%item)[1:-1]

            # Trata item que não está na tabela
            if not self.caracter_reconhecido(item):
                return None

            # Armazena o novo estado
            estado = self.tabela_estados[item][estado]

            # Verifica o proximo estado
            if self.index < self.tam-1:
                
                # Transforma a string para lidar com os \n \t e etc...
                prox_item = ('%r'%self.string[self.index+1])[1:-1]
                
                # Trata item que não está na tabela
                if not self.caracter_reconhecido(prox_item):
                    return None

                # Verifica o proximo estado
                prox_estado = self.tabela_estados[prox_item][estado]
                
            else:
                
                # Se já estiver no final da string, proximo estado é NaN
                prox_estado = float('nan')
                
            # Incrementa o index
            self.index += 1

            # Se o proximo estado for NaN, ou seja inalcançável, retorna o token se não for um espaço
            if prox_estado != prox_estado:

                # Nome do token
                nome = self.tabela_estados['Nome'][estado]

                # Se for um identificador, verifica se eh uma palavra reservada
                if nome == 'ident' and buffer in self.palavras_reservadas:
                    nome = 'reservada'

                # Se o token não for espaço, imprime ele
                if nome != 'espaco':
                    return {
                        'token': buffer,
                        'id_token': nome
                    }
                # Se for um espaço, reseta o buffer e o estado
                else:
                    buffer = ''
                    estado = 0
                    
        # Se acabou o arquivo, retorna None
        return None
