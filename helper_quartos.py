"""Módulo de auxiliar para funções relacionadas às reservas de quartos do hotel.

"""

from helper_db import parse_csv, save_csv
from datetime import date, timedelta
from utils.utils import VERDE, RESET

def print_quartos_disponiveis():
    """Imprime os quartos disponíveis formatados como uma tabela."""
    
    data = parse_csv("quartos.csv")

    print("\n" + "=" * 31)
    print(f"| {'QUARTO':^8} | {'STATUS':^16} |")
    print("=" * 31)

    quartos_livres = 0  # Contador para o nosso teste de disponibilidade

    for quarto in data:

        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            quartos_livres += 1
            num = quarto['QUARTO']

            print(f"| {num:^8} | {VERDE}{'Disponível':^16}{RESET} |")

    #Tratando o caso limite de não haver nenhum quarto disponível
    if quartos_livres == 0:
        print(f"| {'Nenhum quarto livre no momento':^27} |")

    print("-" * 31)


def fazer_checkin(nome: str, quarto_numero: str, dias: str) -> str:
    """Tenta realizar o check-in de um cliente em um quarto específico."""

    data = parse_csv("quartos.csv")
    quarto_disponivel = None

    for quarto in data:
        if quarto["QUARTO"] == quarto_numero:
            # SÓ SALVA A VARIÁVEL SE ESTIVER DISPONÍVEL!
            if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
                quarto_disponivel = quarto

            # O break fica FORA do if de disponibilidade, mas DENTRO do if de número.
            break

    if quarto_disponivel:
        quarto_disponivel["DISPONIBILIDADE"] = "RESERVADO"
        quarto_disponivel["CLIENTE"] = nome
        quarto_disponivel["CHECKIN"] = date.today().isoformat()

        checkout = date.today().fromisoformat(quarto_disponivel["CHECKIN"]) + timedelta(days=int(dias))
        quarto_disponivel["CHECKOUT"] = checkout.isoformat()

        save_csv("quartos.csv", data)

        return f"Check-in realizado com sucesso no quarto {quarto_disponivel['QUARTO']}."

    else:
        return f"O quarto {quarto_numero} não existe ou já está ocupado."
    
def consultar_reserva(nome: str) -> str:
    """Consulta a reserva de um cliente pelo nome."""
    
    data = parse_csv("quartos.csv")
    reservas = []
    
    for quarto in data:
        if quarto["CLIENTE"].strip().lower() == nome.strip().lower():
            reservas.append(quarto)
    
    if not reservas:    
        return "Nenhuma reserva encontrada para o nome fornecido."

    resultado = f"Reservas para {nome}:\n"
    for reserva in reservas:
        resultado += f"Quarto {reserva['QUARTO']} - Check-in: {reserva['CHECKIN']} - Check-out: {reserva['CHECKOUT']}\n"
    return resultado

def cancelar_reserva(nome: str, quarto_numero: str) -> str:
    """Cancela a reserva de um cliente pelo nome e pelo número do quarto."""
    
    data = parse_csv("quartos.csv")
    
    for quarto in data:
        if quarto["CLIENTE"].strip().lower() == nome.strip().lower() and quarto["QUARTO"] == quarto_numero:
            quarto["DISPONIBILIDADE"] = "DISPONÍVEL"
            quarto["CLIENTE"] = ""
            quarto["CHECKIN"] = ""
            quarto["CHECKOUT"] = ""
            
            save_csv("quartos.csv", data)
            
            return f"Reserva cancelada com sucesso para o cliente {nome}."
    
    return "Nenhuma reserva encontrada para o nome fornecido."
