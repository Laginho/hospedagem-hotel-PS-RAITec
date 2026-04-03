from datetime import datetime
from utils.utils import VERMELHO, VERDE, AZUL, AMARELO, NEGRITO, RESET
from helper_db import parse_csv


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
            return numero
        except ValueError:
            # Se quebrar (ex: digitou letra), avisa o erro
            print(f"{AMARELO}ERRO: Digite apenas números inteiros. Letras não são aceitas.{RESET}")


def ler_data(mensagem):
    #Garante que o usuário digite uma data real no formato DD/MM/AAAA.
    while True:
        data_str = input(mensagem).strip()
        if data_str == "":
            print(f"{AMARELO}ERRO: A data é obrigatória.{RESET}")
            continue

        try:
            #O strptime tenta encaixar a string no formato de data
            data_valida = datetime.strptime(data_str, "%d/%m/%Y")

            #Se passar retorna a data bonitinha como string
            return data_valida.strftime("%d/%m/%Y")
        except ValueError:
            print(f"{AMARELO}ERRO: Data inválida ou formato incorreto. Use DD/MM/AAAA{RESET}")


def tem_quarto_disponivel():
    """Verifica no CSV se existe pelo menos um quarto livre."""
    data = parse_csv("quartos.csv")

    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            return True

    return False


def quarto_esta_livre(numero_quarto: str) -> bool:
    """Verifica se um quarto específico existe e está com status 'DISPONÍVEL'."""
    data = parse_csv("quartos.csv")

    for quarto in data:
        # Achou o quarto que o usuário digitou
        if quarto["QUARTO"] == numero_quarto:
            # Retorna True se estiver livre, False se estiver qualquer outra coisa
            return quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL"

    # Se o loop terminar e não achar o número do quarto no CSV, ele não existe
    return False