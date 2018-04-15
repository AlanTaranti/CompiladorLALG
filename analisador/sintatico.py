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

        #self.__busca_token('palavra_reservada', 'integer', printar_erro_sintatico=True)
        pass

    def __mais_var(self):
        pass

    def __dc_p(self):
        pass

    def __parametros(self):
        pass

    def __lista_par(self):
        pass

    def __mais_par(self):
        pass

    def __corpo_p(self):
        pass

    def __dc_loc(self):
        pass

    def __lista_arg(self):
        pass

    def __argumentos(self):
        pass

    def __mais_ident(self):
        pass

    def __pfalsa(self):
        pass

    def __comandos(self):
        pass

