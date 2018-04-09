#
# Analisador Léxico
#
# Desenvolvedor: Alan Taranti
#

class Lexico:
    
    def __init__(self, string):

        import re
        
        # Armazena a string
        self.string = string
        
        # Controle do index
        self.index = 0

        # Controle de linha
        self.linha = 1

        # Remover comentarios
        p = re.compile("\{[\w, ]+\}")
        self.string = p.sub(' ', self.string)

        # Separar end de ponto
        p = re.compile("(end\.)")
        self.string = p.sub('end .', self.string)

        # Separar tokens
        p = re.compile("[^\S\r\n]+|(;|:=|:|\(|\)|,|<|\+|>|-|=|\*|/|\n)")
        self.tokens = p.split(self.string)
        self.tokens = [x for x in self.tokens if x is not None and x is not '']

        # Tamanho
        self.quantidade_de_tokens = len(self.tokens)

        #
        # Tokens
        #

        # Palavras reservadas
        self.tipo_token = dict()

        self.tipo_token['palavra_reservada'] = [
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

        self.tipo_token['especial'] = [
            '*',
            '.',
            ',',
            '=',
            '<',
            '<=',
            '<>',
            '/',
            ';',
            '>',
            '>=',
            ':',
            ':=',
            '(',
            ')',
            '{',
            '}',
            "'",
            '+',
            '-'
        ]

    # Retorna o tipo do token
    def get_tipo_do_token(self, token):

        import re

        if token in self.tipo_token['especial']:
            return token

        if token in self.tipo_token['palavra_reservada']:
            return 'palavra_reservada'

        if re.fullmatch('\d+\.\d+', token):
            return 'real'

        if re.fullmatch('\d+', token):
            return 'integer'

        if re.fullmatch('\w+', token):
            return 'identificador'

        return None

    # Retorna o proximo token
    def get_next_token(self):

        if self.index < self.quantidade_de_tokens:
            token = self.tokens[self.index]
            self.index += 1

            while token == '\n':
                if self.index == self.quantidade_de_tokens:
                    return None
                token = self.tokens[self.index]
                self.index += 1
                self.linha += 1

            tipo_token = self.get_tipo_do_token(token)

            return {
                'token': token,
                'tipo': tipo_token,
                'linha': self.linha
            }

        else:
            return None
