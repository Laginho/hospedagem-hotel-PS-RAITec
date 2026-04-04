from datetime import datetime, date
from utils.utils import VERMELHO, AMARELO, NEGRITO, RESET
from services.helper_db import parse_csv


def ler_texto_obrigatorio(mensagem):
    #Garante que o usuário não deixe o campo em branco.
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print(f"{AMARELO}{NEGRITO}ERRO: Esse campo é obrigatório e não pode ficar vazio.{RESET}")
        else:
            return texto


def ler_numero_inteiro(mensagem):
    #Garante que o usuário digite um número inteiro válido.
    while True:
        valor = input(mensagem).strip()
        if valor == "":
            print(f"{AMARELO}ERRO: Esse campo não pode ficar vazio.{RESET}")
            continue

        try:
            # Tenta converter o texto para inteiro
            numero = int(valor)

            if numero <= 0:
                print(f"{AMARELO}ERRO: A quantidade de dias deve ser maior que zero.{RESET}")
                continue

            return numero
        except ValueError:
            # Se quebrar (ex: digitou letra), avisa o erro
            print(f"{AMARELO}ERRO: Digite apenas números inteiros. Letras não são aceitas.{RESET}")


def ler_data_futura(mensagem: str) -> date:
    """Pede uma data ao usuário e garante que ela seja igual ou maior que hoje."""
    while True:
        data_str = input(mensagem).strip()
        try:
            # Tenta converter a string "DD/MM/AAAA" em um objeto de data do Python
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()

            if data_obj < date.today():
                print(f"{VERMELHO}ERRO: A data de check-in não pode estar no passado!{RESET}")
            else:
                return data_obj  # Retorna a data perfeitinha

        except ValueError:
            print(f"{VERMELHO}ERRO: Formato inválido. Use o formato DD/MM/AAAA.{RESET}")


def tem_quarto_disponivel():
    """Verifica no CSV se existe pelo menos um quarto livre."""
    data = parse_csv("data/quartos.csv")

    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            return True

    return False


def quarto_esta_livre(numero_quarto: str) -> bool:
    """Verifica se um quarto específico existe e está com status 'DISPONÍVEL'."""
    data = parse_csv("data/quartos.csv")

    for quarto in data:
        # Achou o quarto que o usuário digitou
        if quarto["QUARTO"] == numero_quarto:
            # Retorna True se estiver livre, False se estiver qualquer outra coisa
            return quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL"

    # Se o loop terminar e não achar o número do quarto no CSV, ele não existe
    return False

def validar_login(cpf: str, senha: str) -> bool:
    """Verifica se existe um cliente com o CPF e senha fornecidos."""
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf and conta["SENHA"] == senha:
            return True
    return False

def get_nome_cliente(cpf: str) -> str:
    """Dado um CPF, retorna o nome do cliente associado a ele, ou None se não encontrado."""
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf:
            return conta.get("NOME", None)
    return None


def ler_cpf(mensagem: str) -> str:
    """Lê, higieniza e valida o formato básico de um CPF."""
    while True:
        cpf_digitado = input(mensagem).strip()

        if cpf_digitado == "0":
            return "0"

        cpf_limpo = cpf_digitado.replace(".", "").replace("-", "")

        if cpf_limpo == "":
            print(f"{AMARELO}ERRO: O CPF não pode ficar vazio.{RESET}")
            continue

        if len(cpf_limpo) != 11:
            print(f"{AMARELO}ERRO: O CPF deve ter exatamente 11 números. Você digitou {len(cpf_limpo)}.{RESET}")
            continue

        if not cpf_limpo.isdigit():
            print(f"{AMARELO}ERRO: O CPF deve conter apenas números válidos.{RESET}")
            continue

        return cpf_limpo


def cpf_ja_cadastrado(cpf_limpo: str) -> bool:
    """Verifica se o CPF já existe no banco de dados de credenciais."""
    try:
        # Puxa a lista de usuários salvos no arquivo
        usuarios_salvos = parse_csv("data/credenciais.csv")

        # Procura linha por linha se o CPF já está na coluna "USUARIO"
        for usuario in usuarios_salvos:
            if usuario["USUARIO"] == cpf_limpo:
                return True

        return False

    except FileNotFoundError:
        # Se o arquivo CSV ainda não existe, é impossível ter alguém cadastrado
        return False