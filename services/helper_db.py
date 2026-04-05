"""Utilitários de persistência em CSV para usuários e credenciais.

Este módulo centraliza operações de leitura, escrita e consultas simples em
arquivos CSV utilizados pelo sistema de hospedagem.
"""

import csv

def parse_csv(filename: str) -> list:
    """Lê um arquivo CSV e retorna os registros como lista de dicionários.

    Args:
        filename (str): Caminho do arquivo CSV a ser lido.

    Returns:
        list: Coleção em que cada item representa uma linha do arquivo e as
            chaves correspondem aos nomes das colunas.
    """
    
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

#==================================================================================================================
#==================================================================================================================

def print_csv(filename: str) -> None:
    """Imprime os dados de um arquivo CSV em formato tabular simples.

    Args:
        filename (str): Caminho do arquivo CSV a ser exibido.

    A função assume que existe ao menos uma linha de dados no arquivo,
    pois usa o primeiro registro para obter o cabeçalho.
    """
    
    data = parse_csv(filename)
    
    columns = data[0].keys()
    
    print("\t".join(columns))
    
    for row in data:
        print("\t".join(str(row[col]) for col in columns))


# ==================================================================================================================
# ==================================================================================================================

def save_csv(filename: str, data: list) -> None:
    """Persiste dados em um arquivo CSV.

    Args:
        filename (str): Caminho do arquivo CSV de destino.
        data (list): Lista de dicionários a ser salva no arquivo.

    Quando a lista está vazia, o arquivo não é sobrescrito.
    """
    
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        if len(data) == 0:
            return
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

#==================================================================================================================
#==================================================================================================================

def cadastrar_usuario_bd(tipo, nome, cpf, senha, nascimento, endereco):
    """Cadastra um usuário na base de credenciais.

    Args:
        tipo: Tipo de conta, como Cliente ou Funcionário.
        nome: Nome completo do usuário.
        cpf: CPF usado como identificador de login.
        senha: Senha de autenticação da conta.
        nascimento: Data de nascimento no formato adotado pela aplicação.
        endereco: Cidade/estado informado no cadastro.
    """
    contas = parse_csv("data/credenciais.csv")
    contas.append({"TIPO": tipo, "USUARIO": cpf, "SENHA": senha, "NOME": nome, "NASCIMENTO": nascimento, "ENDERECO": endereco})
    save_csv("data/credenciais.csv", contas)

#==================================================================================================================
#==================================================================================================================

def autenticar_usuario_db(cpf, senha, tipo):
    """Autentica um usuário com base em CPF, senha e tipo.

    Args:
        cpf: CPF informado no login.
        senha: Senha informada no login.
        tipo: Perfil esperado para autenticação.

    Returns:
        dict | None: Registro do usuário quando encontrado e validado; caso
            contrário, retorna None.
    """
    contas = parse_csv("data/credenciais.csv")

    for conta in contas:
        if conta["TIPO"] == tipo and conta["USUARIO"] == cpf and conta["SENHA"] == senha:
            return conta

    return None

#==================================================================================================================
#==================================================================================================================

def buscar_nome_cliente_por_cpf(cpf: str):
    """Busca o nome de um cliente a partir do CPF.

    Args:
        cpf (str): CPF do cliente que será consultado.

    Returns:
        str | None: Nome do cliente quando encontrado; None quando não existe
            registro correspondente.
    """
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf:
            return conta["NOME"]
    return None