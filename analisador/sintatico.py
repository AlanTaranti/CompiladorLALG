#
# Analisador Sintático
#
# Desenvolvedor: Alan Taranti
#

from . import Lexico


class Sintatico:

    def __init__(self, string):

        self.__lexico = Lexico(string)
        self.__status_geral = True
        self.__contador_de_erros_lexicos = 0
        self.__contador_de_erros_sintaticos = 0

    def start(self):
        return self.__programa()

    # Método responsável por verificar o próximo token sem andar com a fita
    def __look_ahead_token(self, tipo_esperado, token_esperado=None, consumir=False):

        token = self.__lexico.look_ahead(consumir)

        token['status'] = token['tipo'] == tipo_esperado

        if token_esperado is not None:
            token['status'] = token['status'] and token['token'] == token_esperado

        return token

    # Método responsável por consumir o próximo token da fita
    def __get_token(self, tipo_esperado, token_esperado=None, token_anterior=None, printar_erro_sintatico=True,
                    consumir_se_nao_encontrado=True):

        consumir = True
        if not consumir_se_nao_encontrado:
            token = self.__look_ahead_token(None)
            if token['tipo'] != tipo_esperado or token_esperado is not None and token['token'] != token_esperado:
                consumir = False

        token = self.__lexico.get_next_token(consumir)
        token['status'] = True
        msg = str()

        # Trata nenhum token retornado
        if token['token'] is None:
            token['status'] = False

            if printar_erro_sintatico:
                msg = 'Erro - Linha: ' + str(token['linha']) + '. '
                if token_esperado is not None:
                    msg += 'Esperado token: ' + token_esperado
                else:
                    msg += 'Esperado token do tipo "' + tipo_esperado + '"'
                    msg += ', porém nenhum foi encontrado'

        # Trata token do tipo diferente do informado
        elif token['tipo'] != tipo_esperado:
            token['status'] = False
            if printar_erro_sintatico:
                msg = 'Erro - Linha: ' + str(token['linha']) + '. '
                msg += 'Esperado token do tipo "' + tipo_esperado + '"'
                if token_anterior is not None:
                    msg += ' após ' + token_anterior
                msg += ', porém encontrado do tipo "' + token['tipo'] + '"'

        # Trata token diferente do esperado
        elif token_esperado is not None and token['token'] != token_esperado:
            token['status'] = False
            if printar_erro_sintatico:
                msg = 'Erro - Linha: ' + str(token['linha']) + '. '
                msg += 'Esperado token: ' + token_esperado
                if token_anterior is not None:
                    msg += ' após ' + token_anterior
                msg += ', porém encontrado do tipo "' + token['tipo'] + '"'

        # Contabiliza e informa os erros
        if not token['status']:
            self.__status_geral = False
            self.__contador_de_erros_sintaticos += 1
            self.__contador_de_erros_lexicos += 1 if token['tipo'] == 'desconhecido' else 0
            if printar_erro_sintatico:
                print(msg)

        return token

    # Método responsável por finalizar a compilação
    def __finalizar_programa(self):

        if self.__status_geral:
            msg = 'Programa compilado com sucesso'
            status = True
        else:
            msg = 'Programa com erros \n'
            msg += 'Encontrado um total de ' + str(self.__contador_de_erros_lexicos +
                                                   self.__contador_de_erros_sintaticos) + ' erros \n'
            msg += 'Sendo ' + str(self.__contador_de_erros_lexicos) + ' erros léxicos\n'
            msg += 'E ' + str(self.__contador_de_erros_sintaticos) + ' erros sintáticos\n'
            status = False

        return {
            'mensagem': msg,
            'status': status
        }

    # Trata o não terminal <programa>
    def __programa(self):

        # Busca 'program'
        program = self.__get_token('palavra_reservada', 'program')

        # Se encontrou o 'program', procura um idenficador
        if program['status']:

            # Busca um idenficador
            identificador = self.__get_token('identificador', token_anterior=program['token'])

            # Se encontrou um idenficador, procura um ';'
            if identificador['status']:

                # Busca um ';'
                self.__get_token(';', token_anterior=identificador['token'], consumir_se_nao_encontrado=False)

            else:
                # Else do identificador
                self.__get_token(';', consumir_se_nao_encontrado=False)
        else:
            # Else do program
            self.__get_token(';', consumir_se_nao_encontrado=False)

        # Entra em <corpo>
        self.__corpo()

        # Busca um '.'
        self.__get_token('.')

        # Finaliza graciosamente o programa
        return self.__finalizar_programa()

    # Trata o não terminal <corpo>
    def __corpo(self):

        # Entra em <dc>
        self.__dc()

        # Busca 'begin'
        self.__get_token('palavra_reservada', 'begin')

        # Entra em <comandos>
        self.__comandos()

        # Busca 'end'
        self.__get_token('palavra_reservada', 'end')

    # Trata o não terminal <dc>
    def __dc(self):

        # Entra em <dc_v>
        self.__dc_v()

        # Entra em <dc_p>
        self.__dc_p()

    # Trata o não terminal <dc_v>
    def __dc_v(self, recursao=False):

        # Look Ahead 'var'
        if recursao:
            var = self.__look_ahead_token('palavra_reservada', 'var')
        else:
            var = self.__get_token('palavra_reservada', 'var')

        if var['status']:

            # Get 'var'
            if recursao:
                self.__get_token('palavra_reservada', 'var')

            # Entra em <variaveis>
            self.__variaveis()

            # Busca ':'
            self.__get_token(':')

            # Entra em <tipo_var>
            self.__tipo_var()

            # Busca ';'
            self.__get_token(';', consumir_se_nao_encontrado=False)

            # Entra em <dc_v>
            self.__dc_v(recursao=True)

    # Trata o não terminal <tipo_var>
    def __tipo_var(self):

        # Procurar integer ou real
        integer = self.__look_ahead_token('palavra_reservada', 'integer')
        real = self.__look_ahead_token('palavra_reservada', 'real')

        # Consumir integer, se existir
        if integer['status']:
            self.__get_token('palavra_reservada', 'integer')

        # Consumir real, se existir
        elif real['status']:
            self.__get_token('palavra_reservada', 'real')

        # Informar erro
        else:
            self.__get_token('palavra_reservada', 'integer ou real')

    def __variaveis(self):

        # Buscar identificador
        self.__get_token('identificador')

        # Entra em <mais_var>
        self.__mais_var()

    def __mais_var(self):

        # Look ahead ','
        virgula = self.__look_ahead_token(',')

        if virgula['status']:

            # Consome token
            self.__get_token(',')

            # Entra em <variaveis>
            self.__variaveis()

    def __dc_p(self):

        # Look ahead 'procedure'
        procedure = self.__look_ahead_token('palavra_reservada', 'procedure')

        if procedure['status']:
            self.__get_token('palavra_reservada', 'procedure')
            self.__get_token('identificador')
            self.__parametros()
            self.__get_token(';',consumir_se_nao_encontrado=False)
            self.__corpo_p()
            self.__dc_p()

    def __parametros(self):
        parenteses = self.__look_ahead_token('(')

        if parenteses['status']:
            self.__get_token('(')
            self.__lista_par()
            self.__get_token(')')

    def __lista_par(self):

        self.__variaveis()
        self.__get_token(':')
        self.__tipo_var()
        self.__mais_par()

    def __mais_par(self):

        ponto_virgula = self.__look_ahead_token(';')

        if ponto_virgula['status']:
            self.__get_token(';', consumir_se_nao_encontrado=False)
            self.__lista_par()

    def __corpo_p(self):
        self.__dc_loc()
        self.__get_token('palavra_reservada', 'begin')
        self.__comandos()
        self.__get_token('palavra_reservada', 'end')
        self.__get_token(';', consumir_se_nao_encontrado=False)

    def __dc_loc(self):
        self.__dc_v()

    def __lista_arg(self):
        parenteses = self.__look_ahead_token('(')

        if parenteses['status']:
            self.__get_token('(')
            self.__argumentos()
            self.__get_token(')')

    def __argumentos(self):
        self.__get_token('identificador')
        self.__mais_ident()

    def __mais_ident(self):

        ponto_virgula = self.__look_ahead_token(';')

        if ponto_virgula['status']:
            self.__get_token(';', consumir_se_nao_encontrado=False)
            self.__argumentos()

    def __pfalsa(self):
        else_token = self.__look_ahead_token('palavra_reservada', 'else')

        if else_token['status']:
            self.__get_token('palavra_reservada', 'else')
            self.__cmd()

    def __comandos(self):

        status = self.__cmd()
        if status:
            self.__get_token(';', consumir_se_nao_encontrado=False)
            self.__comandos()

    def __cmd(self):

        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] == 'identificador':
            self.__get_token('identificador')
            atribuicao = self.__look_ahead_token(':=')

            if atribuicao['status']:
                self.__get_token(':=')
                self.__expressao()
            else:
                self.__lista_arg()

            return True
        elif resposta['tipo'] == 'palavra_reservada':

            if resposta['token'] in ['read', 'write']:
                self.__look_ahead_token(None, consumir=True)
                self.__get_token('(')
                self.__variaveis()
                self.__get_token(')')
            elif resposta['token'] == 'while':
                self.__look_ahead_token(None, consumir=True)
                self.__condicao()
                self.__get_token('palavra_reservada', 'do')
                self.__cmd()
            elif resposta['token'] == 'if':
                self.__look_ahead_token(None, consumir=True)
                self.__condicao()
                self.__get_token('palavra_reservada', 'then')
                self.__cmd()
                self.__pfalsa()
            elif resposta['token'] == 'begin':
                self.__look_ahead_token(None, consumir=True)
                self.__comandos()
                self.__get_token('palavra_reservada', 'end')
            else:
                return False
            return True
        else:
            return False

    def __condicao(self):
        self.__expressao()
        self.__relacao()
        self.__expressao()

    def __relacao(self):
        tipos_aceitos = ['=', '<>', '>=', '<=', '>', '<']

        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] in tipos_aceitos:
            self.__look_ahead_token(None, consumir=True)

    def __expressao(self):
        self.__termo()
        self.__outros_termos()

    def __op_un(self):
        tipos_aceitos = ['+', '-']

        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] in tipos_aceitos:
            self.__look_ahead_token(None, consumir=True)

    def __outros_termos(self):
        resposta = self.__op_ad()
        if resposta:
            self.__termo()
            self.__outros_termos()

    def __op_ad(self):
        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] in ['+', '-']:
            self.__look_ahead_token(None, consumir=True)
        else:
            return False
        return True

    def __termo(self):
        self.__op_un()
        self.__fator()
        self.__mais_fatores()

    def __mais_fatores(self):
        resposta = self.__op_mul()
        if resposta:
            self.__fator()
            self.__mais_fatores()

    def __op_mul(self):
        tipos_aceitos = ['*', '/']

        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] in tipos_aceitos:
            self.__look_ahead_token(None, consumir=True)
            return True
        return False

    def __fator(self):
        tipos_consumiveis = ['identificador', 'integer', 'real']

        resposta = self.__look_ahead_token(None)

        if resposta['tipo'] in tipos_consumiveis:
            self.__look_ahead_token(None, consumir=True)
        elif resposta['tipo'] == '(':
            self.__look_ahead_token(None, consumir=True)
            self.__expressao()
            self.__get_token(')')
        else:
            return False
        return True

