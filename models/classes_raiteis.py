"""Modelos de domínio para usuários, reservas e quartos.

Este módulo centraliza as entidades de negócio utilizadas pelo sistema de
hospedagem. As classes são simples, focadas em representar estado e expor
operações básicas usadas pela camada de interface.

Nota:
    A persistência principal da aplicação ocorre em arquivos CSV. Por isso,
    alguns métodos desta camada fazem validações lendo diretamente esses dados,
    principalmente por compatibilidade com fluxos legados.
"""

from abc import ABC
from datetime import date, timedelta

from services.helper_db import parse_csv


class Usuario(ABC):
    """Classe base para os perfis de usuário do sistema.

    Attributes:
        nome (str): Nome completo do usuário.
        cpf (str): CPF utilizado como identificador único de login.
        senha (str): Senha cadastrada para autenticação.
        tipo (str): Tipo do usuário na aplicação.
    """

    def __init__(self, nome: str, cpf: str, senha: str) -> None:
        """Inicializa os atributos comuns de um usuário.

        Args:
            nome (str): Nome completo do usuário.
            cpf (str): CPF no formato numérico em string.
            senha (str): Senha de acesso.
        """
        self.nome = nome
        self.senha = senha
        self.cpf = cpf
        self.tipo = "Nenhum"

    def validar_login(self, senha: str) -> bool:
        """Valida credenciais do usuário na base CSV.

        Este método é mantido por compatibilidade com implementações anteriores,
        embora o fluxo principal de autenticação hoje esteja na camada de
        serviços.

        Args:
            senha (str): Senha informada na tentativa de login.

        Returns:
            bool: True quando tipo, CPF e senha correspondem a um registro;
                caso contrário, False.
        """
        contas = parse_csv("data/credenciais.csv")
        for conta in contas:
            if conta["TIPO"] == self.tipo and conta["USUARIO"] == self.cpf and conta["SENHA"] == senha:
                return True
        return False


class Funcionario(Usuario):
    """Representa um usuário com perfil de administração do hotel."""

    def __init__(self, nome: str, cpf: str, senha: str) -> None:
        """Cria um funcionário e define o tipo de acesso administrativo.

        Args:
            nome (str): Nome completo do funcionário.
            cpf (str): CPF do funcionário.
            senha (str): Senha de acesso.
        """
        super().__init__(nome, cpf, senha)
        self.tipo = "Funcionário"


class Cliente(Usuario):
    """Representa um hóspede com acesso ao portal de cliente.

    Attributes:
        reservas (list): Coleção mantida por compatibilidade com versões
            antigas, onde reservas eram associadas diretamente ao objeto cliente.
    """

    def __init__(self, nome: str, cpf: str, senha: str) -> None:
        """Cria um cliente com perfil de acesso ao portal de hóspedes.

        Args:
            nome (str): Nome completo do cliente.
            cpf (str): CPF do cliente.
            senha (str): Senha de acesso.
        """
        super().__init__(nome, cpf, senha)
        self.tipo = "Cliente"
        self.reservas = []

    def getNome(self) -> str:
        """Retorna o nome do cliente.

        Returns:
            str: Nome completo do cliente.
        """
        return self.nome

    def getCPF(self) -> str:
        """Retorna o CPF do cliente.

        Returns:
            str: CPF associado ao cliente.
        """
        return self.cpf

    def getReservas(self) -> list:
        """Retorna a lista de reservas vinculadas ao objeto cliente.

        Returns:
            list: Lista de reservas mantida em memória.
        """
        return self.reservas

    def addReserva(self, reserva) -> None:
        """Adiciona uma reserva à coleção local do cliente.

        Args:
            reserva: Objeto de reserva a ser adicionado.
        """
        self.reservas.append(reserva)


class Reserva:
    """Representa uma reserva de quarto com período definido.

    Attributes:
        quarto (str): Identificador do quarto reservado.
        checkin (date): Data de entrada.
        checkout (date): Data de saída calculada a partir do check-in e duração.
    """

    def __init__(self, quarto: str, data_inicio, dias: int) -> None:
        """Inicializa uma reserva e calcula a data de checkout.

        Args:
            quarto (str): Número ou identificador do quarto.
            data_inicio: Data de check-in em objeto date ou string ISO
                (AAAA-MM-DD).
            dias (int): Quantidade de dias reservados.
        """
        self.quarto = quarto
        if isinstance(data_inicio, str):
            data_inicio = date.fromisoformat(data_inicio)
        self.checkin = data_inicio
        self.checkout = data_inicio + timedelta(days=dias)

    def getQuarto(self) -> str:
        """Retorna o quarto associado à reserva.

        Returns:
            str: Identificador do quarto.
        """
        return self.quarto

    def getCheckin(self) -> date:
        """Retorna a data de check-in.

        Returns:
            date: Data de entrada da reserva.
        """
        return self.checkin

    def getCheckout(self) -> date:
        """Retorna a data de checkout.

        Returns:
            date: Data de saída da reserva.
        """
        return self.checkout


class Quarto:
    """Representa um quarto do hotel e seu estado operacional.

    Attributes:
        numero (str): Número identificador do quarto.
        diaria (int): Valor da diária em reais.
        condicao (str): Estado atual do quarto (inicialmente "Disponível").
    """

    def __init__(self, numero, diaria) -> None:
        """Cria um quarto com número, diária e condição padrão.

        Args:
            numero: Número identificador do quarto.
            diaria: Valor da diária do quarto.
        """
        self.numero = str(numero)
        self.diaria = int(diaria)
        self.condicao = "Disponível"

    def getNumero(self) -> str:
        """Retorna o número do quarto.

        Returns:
            str: Número identificador do quarto.
        """
        return self.numero

    def getCondicao(self) -> str:
        """Retorna a condição atual do quarto.

        Returns:
            str: Estado operacional do quarto.
        """
        return self.condicao
