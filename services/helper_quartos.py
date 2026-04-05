"""Serviços de gestão de quartos, reservas e checkout.

Este módulo reúne operações de consulta, exibição e atualização da base de
quartos utilizada pelos fluxos de cliente e funcionário.
"""

from services.helper_db import parse_csv, save_csv
from datetime import date, timedelta
from utils.utils import VERDE, RESET, VERMELHO, AMARELO


def print_todos_os_quartos():
    """Exibe todos os quartos cadastrados com status e valor de diária.

    Esta visualização é utilizada principalmente pelos fluxos de administração.
    """
    data = parse_csv("data/quartos.csv")

    print("\n" + "=" * 46)
    print(f"| {'QUARTO':^8} | {'STATUS':^16} | {'DIÁRIA (R$)':^11} |")
    print("=" * 46)

    for quarto in data:
        num = quarto['QUARTO']
        status = quarto['DISPONIBILIDADE'].strip().upper()


        preco = float(quarto.get("DIARIA", "0") or "0")


        if status == "DISPONÍVEL":
            status_colorido = f"{VERDE}{status.capitalize():^16}{RESET}"
        elif status == "RESERVADO":
            status_colorido = f"{VERMELHO}{status.capitalize():^16}{RESET}"
        else:
            status_colorido = f"{AMARELO}{status.capitalize():^16}{RESET}"

        print(f"| {num:^8} | {status_colorido} | R$ {preco:>8.2f} |")

    print("-" * 46)

#==================================================================================================================
#==================================================================================================================

def print_quartos_disponiveis():
    """Exibe apenas os quartos com disponibilidade para reserva.

    Quando não há quartos livres, informa explicitamente a indisponibilidade.
    """

    data = parse_csv("data/quartos.csv")


    print("\n" + "=" * 46)
    print(f"| {'QUARTO':^8} | {'STATUS':^16} | {'DIÁRIA (R$)':^11} |")
    print("=" * 46)

    quartos_livres = 0

    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            quartos_livres += 1
            num = quarto['QUARTO']

            valor_bruto = quarto.get("DIARIA", "0") or "0"
            preco = float(valor_bruto)

            print(f"| {num:^8} | {VERDE}{'Disponível':^16}{RESET} | R$ {preco:>8.2f} |")

    if quartos_livres == 0:
        print(f"| {'Nenhum quarto livre no momento':^42} |")

    print("-" * 46)

#==================================================================================================================
#==================================================================================================================

def fazer_checkin(nome: str, cpf: str, quarto_numero: str, dias: str, data_entrada: date) -> str:
    """Realiza o check-in de um cliente em um quarto específico.

    Args:
        nome (str): Nome do cliente responsável pela reserva.
        cpf (str): CPF do cliente associado ao quarto.
        quarto_numero (str): Número do quarto escolhido.
        dias (str): Quantidade de dias da hospedagem.
        data_entrada (date): Data prevista para o check-in.

    Returns:
        str: Mensagem de sucesso com o valor total da estadia, ou mensagem de
            falha quando o quarto não existe ou não está disponível.
    """

    data = parse_csv("data/quartos.csv")
    quarto_disponivel = None

    for quarto in data:
        if quarto["QUARTO"] == quarto_numero:

            if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
                quarto_disponivel = quarto


            break

    if quarto_disponivel:
        quarto_disponivel["DISPONIBILIDADE"] = "RESERVADO"
        quarto_disponivel["CLIENTE"] = nome
        quarto_disponivel["USUARIO"] = cpf
        quarto_disponivel["CHECKIN"] = data_entrada.isoformat()

        checkout = date.today().fromisoformat(quarto_disponivel["CHECKIN"]) + timedelta(days=int(dias))
        quarto_disponivel["CHECKOUT"] = checkout.isoformat()

        save_csv("data/quartos.csv", data)

        valor_diaria = float(quarto_disponivel.get("DIARIA", 0))
        valor_total = valor_diaria * int(dias)

        return f"Check-in realizado! Quarto {quarto_disponivel['QUARTO']} reservado por {dias} dias. Total a pagar: R$ {valor_total:.2f}"

    else:
        return f"O quarto {quarto_numero} não existe ou já está ocupado."

#==================================================================================================================
#==================================================================================================================

def consultar_reserva(nome: str, cpf: str) -> str:
    """Consulta reservas de um cliente e calcula o total por estadia.

    Args:
        nome (str): Nome usado no cabeçalho do relatório de retorno.
        cpf (str): CPF utilizado para filtrar as reservas.

    Returns:
        str: Resumo textual das reservas encontradas com período e valor total.
    """

    data = parse_csv("data/quartos.csv")
    reservas = []

    for quarto in data:
        if quarto["USUARIO"].strip().lower() == cpf.strip().lower():
            reservas.append(quarto)
    # alterei pra buscar por cpfs

    if not reservas:
        return "Nenhuma reserva encontrada para o nome fornecido."

    resultado = f"Reservas para {nome}:\n"

    for reserva in reservas:

        data_in = date.fromisoformat(reserva['CHECKIN'])
        data_out = date.fromisoformat(reserva['CHECKOUT'])


        dias_hospedados = (data_out - data_in).days


        valor_diaria = float(reserva.get("DIARIA", 0))
        valor_total = valor_diaria * dias_hospedados


        resultado += (f" > Quarto {reserva['QUARTO']} | "
                      f"Check-in: {reserva['CHECKIN']} | "
                      f"Check-out: {reserva['CHECKOUT']} | "
                      f"Total a pagar: R$ {valor_total:.2f}\n")

    return resultado

#==================================================================================================================
#==================================================================================================================

def cancelar_reserva(nome: str, cpf: str, quarto_numero: str) -> str:
    """Cancela uma reserva ativa e libera o quarto informado.

    Args:
        nome (str): Nome do cliente para mensagem de confirmação.
        cpf (str): CPF associado à reserva.
        quarto_numero (str): Número do quarto a ser cancelado.

    Returns:
        str: Mensagem confirmando cancelamento ou ausência de reserva
            compatível com os dados informados.
    """
    
    data = parse_csv("data/quartos.csv")
    # alterei pra buscar por cpfs
    for quarto in data:
        if quarto["USUARIO"].strip().lower() == cpf.strip().lower() and quarto["QUARTO"] == quarto_numero:
            quarto["DISPONIBILIDADE"] = "DISPONÍVEL"
            quarto["CLIENTE"] = ""
            quarto["USUARIO"] = ""
            quarto["CHECKIN"] = ""
            quarto["CHECKOUT"] = ""
            
            save_csv("data/quartos.csv", data)
            
            return f"Reserva cancelada com sucesso para o cliente {nome}."
    
    return "Nenhuma reserva encontrada para o nome fornecido."

#==================================================================================================================
#==================================================================================================================

def adicionar_quarto_db(numero_quarto: str, preco_diaria: float) -> bool:
    """Adiciona um novo quarto na base de dados.

    Args:
        numero_quarto (str): Identificador do quarto.
        preco_diaria (float): Valor da diária do novo quarto.

    Returns:
        bool: True quando o quarto é adicionado; False quando já existe um
            registro com o mesmo número.
    """
    data = parse_csv("data/quartos.csv")


    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            return False


    novo_quarto = {
        "QUARTO": numero_quarto,
        "DISPONIBILIDADE": "DISPONÍVEL",
        "CLIENTE": "",
        "USUARIO": "",
        "CHECKIN": "",
        "CHECKOUT": "",
        "DIARIA": f"{preco_diaria:.2f}"
    }

    data.append(novo_quarto)
    save_csv("data/quartos.csv", data)

    return True

#==================================================================================================================
#==================================================================================================================

def alterar_preco_quarto_db(numero_quarto: str, novo_preco: float):
    """Atualiza o valor da diária de um quarto existente.

    Args:
        numero_quarto (str): Número do quarto que será atualizado.
        novo_preco (float): Novo valor da diária.

    Este método assume que as validações de negócio já foram realizadas.
    """
    data = parse_csv("data/quartos.csv")
    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            quarto["DIARIA"] = f"{novo_preco:.2f}"
            save_csv("data/quartos.csv", data)
            return

#==================================================================================================================
#==================================================================================================================

def verificar_status_quarto(numero_quarto: str) -> str:
    """Consulta o status operacional de um quarto.

    Args:
        numero_quarto (str): Número do quarto consultado.

    Returns:
        str: Status do quarto em caixa alta quando encontrado, ou
            NAO_ENCONTRADO quando não existe registro.
    """
    data = parse_csv("data/quartos.csv")
    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            return quarto["DISPONIBILIDADE"].strip().upper()
    return "NAO_ENCONTRADO"


#==================================================================================================================
#==================================================================================================================


def alterar_status_quarto_db(numero_quarto: str, novo_status: str):
    """Atualiza o status de disponibilidade de um quarto.

    Args:
        numero_quarto (str): Número do quarto que será atualizado.
        novo_status (str): Novo status a ser salvo no registro.
    """
    data = parse_csv("data/quartos.csv")
    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            quarto["DISPONIBILIDADE"] = novo_status
            save_csv("data/quartos.csv", data)
            return

#==================================================================================================================
#==================================================================================================================

def excluir_quarto_db(numero_quarto: str):
    """Exclui um quarto da base de dados.

    Args:
        numero_quarto (str): Número do quarto que será removido.
    """
    data = parse_csv("data/quartos.csv")

    data_atualizada = [quarto for quarto in data if quarto["QUARTO"] != numero_quarto]

    save_csv("data/quartos.csv", data_atualizada)

#==================================================================================================================
#==================================================================================================================

def obter_quarto_db(numero_quarto: str):
    """Obtém os dados completos de um quarto.

    Args:
        numero_quarto (str): Número do quarto desejado.

    Returns:
        dict | None: Dicionário com os dados do quarto quando encontrado; caso
            contrário, retorna None.
    """
    data = parse_csv("data/quartos.csv")
    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            return quarto
    return None

#==================================================================================================================
#==================================================================================================================

def liberar_quarto_db(numero_quarto: str):
    """Libera um quarto após checkout, limpando os dados da reserva.

    Args:
        numero_quarto (str): Número do quarto a ser disponibilizado novamente.

    Além de marcar como DISPONÍVEL, remove cliente, usuário, check-in e
    checkout do registro.
    """
    data = parse_csv("data/quartos.csv")
    for quarto in data:
        if quarto["QUARTO"] == numero_quarto:
            quarto["DISPONIBILIDADE"] = "DISPONÍVEL"
            quarto["CLIENTE"] = ""
            quarto["USUARIO"] = ""
            quarto["CHECKIN"] = ""
            quarto["CHECKOUT"] = ""
            save_csv("data/quartos.csv", data)
            return