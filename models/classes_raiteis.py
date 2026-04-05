from datetime import date, timedelta
from services.helper_db import parse_csv
from abc import ABC

#==================================================================================================================
#   MODELAGEM DO ACESSO/CADASTRO DE FUNCIONÁRIOS E CLIENTES (COM ABERTURA PARA ADIÇÃO DE NOVOS TIPOS).
#==================================================================================================================

#   CLASSE ABSTRATA PARA IMPOSSIBILITAR A CRIAÇÃO DO GENÉRICO USUÁRIO
class Usuario(ABC):
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.senha = senha
        self.cpf = cpf
        self.tipo = "Nenhum"
    # ESSE MÉTOODO DE VALIDAR LOGIN ACABOU FICANDO OBSOLETO ATRAVÉS DO USO DO CSV
    def validar_login(self, senha):
        contas = parse_csv("data/credenciais.csv")
        for conta in contas:
            if conta["TIPO"] == self.tipo and conta["USUARIO"] == self.cpf and conta["SENHA"] == senha:
                return True
        return False

#   MODELAGEM DO FUNCIONÁRIO, RESPONSÁVEL PELA ADMISTRAÇÃO
class Funcionario(Usuario):
    def __init__(self, nome, cpf, senha):
        super().__init__(nome, cpf, senha)
        self.tipo = "Funcionário"

#   MODELAGEM DO CLIENTE (HÓSPEDE)
class Cliente(Usuario):
    def __init__(self, nome, cpf, senha):
        super().__init__(nome, cpf, senha)
        self.tipo = "Cliente"
        # ATRIBUTO OBSOLETO QUE DEVIA GUARDAR OBJETOS DO TIPO RESERVA
        self.reservas = []

    # MÉTOODOS USADOS PARA O CHECKIN
    def getNome(self): return self.nome
    def getCPF(self): return self.cpf
    # MÉTODOS RELACIONADOS AO ATRIBUTO OBSOLETO
    def getReservas(self): return self.reservas
    def addReserva(self, reserva):
        self.reservas.append(reserva)

#==================================================================================================================
#   MODELAGEM DAS RESERVAS E DOS QUARTOS, CASO FOSSE NECESSÁRIO.
#==================================================================================================================

#   MODELAGEM DAS RESERVAS
class Reserva:
    def __init__(self, quarto, data_inicio, dias):
        self.quarto = quarto
        # CONVERSÃO DA DATA PARA OBJETO SE FOR RECEBIDA EM STRING
        if isinstance(data_inicio, str):
            data_inicio = date.fromisoformat(data_inicio)
        self.checkin = data_inicio
        # CALCULO DO DIA QUE SERÁ O CHECKOUT
        self.checkout = data_inicio + timedelta(days=dias)

    def getQuarto(self): return self.quarto
    def getCheckin(self): return self.checkin
    def getCheckout(self): return self.checkout

#   MODELAGEM DOS QUARTOS
class Quarto:
    def __init__(self, numero, diaria):
        self.numero = str(numero)
        self.diaria = int(diaria)
        self.condicao = "Disponível"

    def getNumero(self): return self.numero
    def getCondicao(self): return self.condicao


#cpf é em int ou em string????? duvida cruel (COMENTÁRIO LEGAL)
