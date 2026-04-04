"""Módulo de auxiliar de banco de dados para manipulação de arquivos CSV.

O arquivo será da forma QUARTO | DISPONÍVEL/RESERVADO/OCUPADO | CLIENTE | CHECKIN | CHECKOUT

Funções:
    parse_csv(filename): Lê um arquivo CSV e retorna seu conteúdo como uma lista de dicionários.
    save_csv(filename, data): Salva dados em um arquivo CSV.
"""

import csv

def parse_csv(filename: str) -> list:
    """Analisa um arquivo CSV e retorna seu conteúdo como uma lista de dicionários.
    
    Args:
        filename (str): O caminho do arquivo CSV a ser lido.
    Returns:
        list: Uma lista de dicionários, onde cada dicionário representa uma linha
              do arquivo CSV, com as chaves sendo os nomes das colunas definidas
              na primeira linha do arquivo.
    """
    
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]

#==================================================================================================================
#==================================================================================================================

def print_csv(filename: str) -> None:
    """Imprime os dados de um arquivo CSV formatados como uma tabela.
    
    Args:
        filename (str): O caminho do arquivo CSV a ser impresso.
    """
    
    data = parse_csv(filename)
    
    columns = data[0].keys()
    
    print("\t".join(columns))
    
    for row in data:
        print("\t".join(str(row[col]) for col in columns))


# ==================================================================================================================
# ==================================================================================================================

def save_csv(filename: str, data: list) -> None:
    """Salva dados em um arquivo CSV.
    
    Args:
        filename (str): O caminho do arquivo CSV a ser salvo.
        data (list): Uma lista de dicionários, onde cada dicionário representa uma linha
                     a ser salva no arquivo CSV, com as chaves sendo os nomes das colunas.
    """
    
    with open(filename, mode='w', encoding='utf-8', newline='') as file:
        if len(data) == 0:
            return
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

#==================================================================================================================
#==================================================================================================================

def cadastrar_usuario_bd(tipo, nome, cpf, senha):
    """Função coringa para cadastrar Cliente ou Funcionário no banco."""
    contas = parse_csv("data/credenciais.csv")
    contas.append({"TIPO": tipo, "USUARIO": cpf, "SENHA": senha, "NOME": nome})
    save_csv("data/credenciais.csv", contas)

#==================================================================================================================
#==================================================================================================================

def autenticar_usuario_db(cpf, senha, tipo):
    """Busca o usuário no CSV e verifica se a senha e o tipo batem."""
    contas = parse_csv("data/credenciais.csv")

    for conta in contas:
        if conta["TIPO"] == tipo and conta["USUARIO"] == cpf and conta["SENHA"] == senha:
            return conta

    return None  #

#==================================================================================================================
#==================================================================================================================

def buscar_nome_cliente_por_cpf(cpf: str):
    """Busca um cliente pelo CPF e retorna o nome. Retorna None se não achar."""
    contas = parse_csv("data/credenciais.csv")
    for conta in contas:
        if conta["TIPO"] == "Cliente" and conta["USUARIO"] == cpf:
            return conta["NOME"]
    return None