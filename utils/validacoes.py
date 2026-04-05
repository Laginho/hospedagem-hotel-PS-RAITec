"""Funções de validação e normalização de entrada para a interface CLI.

Este módulo concentra regras de consistência dos dados informados pelo usuário
antes de acionar os serviços de negócio e persistência em CSV.
"""

from datetime import datetime, date
from utils.utils import VERMELHO, AMARELO, NEGRITO, RESET
from services.helper_db import parse_csv


def ler_texto_obrigatorio(mensagem):
    """Lê um texto obrigatório, bloqueando entradas vazias.

    Args:
        mensagem: Texto exibido no prompt de entrada.

    Returns:
        str: Conteúdo digitado pelo usuário sem espaços nas extremidades.
    """
    #Garante que o usuário não deixe o campo em branco.
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print(f"{AMARELO}{NEGRITO}ERRO: Esse campo é obrigatório e não pode ficar vazio.{RESET}")
        else:
            return texto


def ler_numero_inteiro(mensagem):
    """Lê um número inteiro positivo para uso em fluxos da aplicação.

    Args:
        mensagem: Texto exibido no prompt de entrada.

    Returns:
        int: Número inteiro maior que zero validado pelo usuário.
    """
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
    """Lê uma data e valida se ela não está no passado.

    Args:
        mensagem (str): Texto exibido no prompt de entrada.

    Returns:
        date: Data válida no formato de objeto date.
    """
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
    """Verifica se existe ao menos um quarto DISPONÍVEL na base.

    Returns:
        bool: True quando há quarto livre; False quando todos os quartos estão
            indisponíveis.
    """
    data = parse_csv("data/quartos.csv")

    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            return True

    return False


def quarto_esta_livre(numero_quarto: str) -> bool:
    """Valida se um quarto específico existe e está disponível.

    Args:
        numero_quarto (str): Número do quarto consultado.

    Returns:
        bool: True quando o quarto existe e está DISPONÍVEL; False nos demais
            casos.
    """
    data = parse_csv("data/quartos.csv")

    for quarto in data:
        # Achou o quarto que o usuário digitou
        if quarto["QUARTO"] == numero_quarto:
            # Retorna True se estiver livre, False se estiver qualquer outra coisa
            return quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL"

    # Se o loop terminar e não achar o número do quarto no CSV, ele não existe
    return False

def validar_login(cpf: str, senha: str) -> bool:
    """Valida credenciais de login para contas de cliente.

    Args:
        cpf (str): CPF informado no login.
        senha (str): Senha informada no login.

    Returns:
        bool: True quando existe cliente com CPF e senha correspondentes;
            False caso contrário.
    """
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf and conta["SENHA"] == senha:
            return True
    return False

def get_nome_cliente(cpf: str) -> str:
    """Retorna o nome do cliente associado ao CPF informado.

    Args:
        cpf (str): CPF do cliente a ser consultado.

    Returns:
        str | None: Nome do cliente quando encontrado; None quando não houver
            registro correspondente.
    """
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf:
            return conta.get("NOME", None)
    return None


def ler_cpf(mensagem: str) -> str:
    """Lê, higieniza e valida o formato básico de um CPF.

    Args:
        mensagem (str): Texto exibido no prompt de entrada.

    Returns:
        str: CPF com 11 dígitos numéricos, sem pontuação.
    """
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
    """Verifica se um CPF já está cadastrado na base de credenciais.

    Args:
        cpf_limpo (str): CPF sem formatação.

    Returns:
        bool: True quando o CPF já existe no cadastro; False caso contrário.
    """
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



def ler_data_nascimento(mensagem: str) -> str:
    """Lê e valida data de nascimento no formato DD/MM/AAAA.

    Args:
        mensagem (str): Texto exibido no prompt de entrada.

    Returns:
        str: Data de nascimento válida no formato DD/MM/AAAA.
    """
    while True:
        data_str = input(mensagem).strip()
        try:
            data_obj = datetime.strptime(data_str, "%d/%m/%Y").date()
            hoje = date.today()

            if data_obj >= hoje:
                print(f"{VERMELHO}ERRO: A data de nascimento deve estar no passado!{RESET}")
                continue

            # Validação extra de sanidade (evitar que a pessoa coloque que nasceu em 1800)
            idade = hoje.year - data_obj.year - ((hoje.month, hoje.day) < (data_obj.month, data_obj.day))
            if idade > 120 or idade < 0:
                print(f"{VERMELHO}ERRO: Data de nascimento irreal.{RESET}")
                continue

            return data_str # Retornamos a string para salvar direto no CSV
        except ValueError:
            print(f"{VERMELHO}ERRO: Formato inválido. Use o formato DD/MM/AAAA.{RESET}")




def ler_endereco(mensagem: str) -> str:
    """Lê e valida endereço no padrão Cidade - UF.

    Args:
        mensagem (str): Texto exibido no prompt de entrada.

    Returns:
        str: Endereço padronizado no formato Cidade - UF.
    """
    estados_validos = [
        "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS",
        "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC",
        "SP", "SE", "TO"
    ]

    while True:
        endereco = input(mensagem).strip()

        # Tenta dividir o que o usuário digitou usando o hífen como corte
        partes = endereco.split("-")

        # Se não tiver exatamente 2 partes (cidade de um lado, estado do outro), dá erro
        if len(partes) != 2:
            print(f"{AMARELO}ERRO: O formato deve ser 'Cidade - UF'. Exemplo: Fortaleza - CE{RESET}")
            continue

        cidade = partes[0].strip()
        uf = partes[1].strip().upper()

        if len(cidade) < 3:
            print(f"{AMARELO}ERRO: O nome da cidade '{cidade}' está muito curto.{RESET}")
            continue

        if uf not in estados_validos:
            print(f"{AMARELO}ERRO: '{uf}' não é uma sigla de estado válida no Brasil.{RESET}")
            continue

        # Se passou em tudo, retorna o formato perfeitinho e padronizado
        return f"{cidade} - {uf}"