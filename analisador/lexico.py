#
# Analisador Léxico
#
# Desenvolvedor: Alan Taranti
#


class Lexico:
    
    def __init__(self, string):

        import re
        
        # Armazena a string
        self.__string = string
        
        # Controle do index
        self.__index = 0

        # Controle de linha
        self.__linha = 1

        # Remover comentarios
        p = re.compile("\{[\w, ]+\}")
        self.__string = p.sub(' ', self.__string)

        # Separar end de ponto
        p = re.compile("(end\.)")
        self.__string = p.sub('end .', self.__string)

        # Separar tokens
        p = re.compile("[^\S\r\n]+|(;|:=|:|\(|\)|,|<|\+|>|-|=|\*|/|\n)")
        self.__tokens = p.split(self.__string)
        self.__tokens = [x for x in self.__tokens if x is not None and x is not '']

        # Tamanho
        self.__quantidade_de_tokens = len(self.__tokens)

        #
        # Tokens
        #

        # Palavras reservadas
        self.__tipo_token = dict()

        self.__tipo_token['palavra_reservada'] = [
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
                'do'
        ]

        self.__tipo_token['especial'] = [
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
    def __get_tipo_do_token(self, token):

        import re

        if token in self.__tipo_token['especial']:
            return token

        if token in self.__tipo_token['palavra_reservada']:
            return 'palavra_reservada'

        if re.fullmatch('\d+\.\d+', token):
            return 'real'

        if re.fullmatch('\d+', token):
            return 'integer'

        if re.fullmatch('\w+', token):
            return 'identificador'

        return 'desconhecido'

    # Retorna o proximo token
    def get_next_token(self, consumir=True):
        return self.__get_next_token(not consumir)

    # Look Ahead
    def look_ahead(self, consumir=False):
        return self.__get_next_token(look_ahead=not consumir)

    # Retorna o proximo token
    def __get_next_token(self, look_ahead=False):

        index = self.__index
        linha = self.__linha

        if index < self.__quantidade_de_tokens:
            token = self.__tokens[index]
            index += 1

            while token == '\n':
                if index == self.__quantidade_de_tokens:

                    if not look_ahead:
                        self.__index = index
                        self.__linha = linha

                    return {
                        'token': None,
                        'tipo': None,
                        'linha': linha
                    }
                token = self.__tokens[index]
                index += 1
                linha += 1

            tipo_token = self.__get_tipo_do_token(token)

            if not look_ahead:
                self.__index = index
                self.__linha = linha

            return {
                'token': token,
                'tipo': tipo_token,
                'linha': linha
            }

        else:

            if not look_ahead:
                self.__index = index
                self.__linha = linha

            return {
                'token': None,
                'tipo': None,
                'linha': linha
            }
