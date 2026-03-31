"""Módulo de auxiliar para funções relacionadas às reservas de quartos do hotel.

"""

from helper_db import parse_csv, save_csv
from datetime import date, timedelta

def print_quartos_disponiveis():
    """Imprime os quartos disponíveis formatados como uma tabela."""
    
    data = parse_csv("quartos.csv")
    
    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            print(f"Quarto {quarto['QUARTO']} - Disponível")
    
def fazer_checkin(nome: str, dias: str) -> str:
    """Realiza o check-in de um cliente em um quarto disponível."""
    
    data = parse_csv("quartos.csv")
    quarto_disponível = None
    
    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            quarto_disponível = quarto
            break

    if quarto_disponível:
        quarto_disponível["DISPONIBILIDADE"] = "RESERVADO"
        quarto_disponível["CLIENTE"] = nome
        quarto_disponível["CHECKIN"] = date.today().isoformat()
        
        checkout = date.today().fromisoformat(quarto_disponível["CHECKIN"]) + timedelta(days=int(dias))
        quarto_disponível["CHECKOUT"] = checkout.isoformat()
        
        save_csv("quartos.csv", data)
        
        return f"Check-in realizado com sucesso no quarto {quarto_disponível['QUARTO']}."
    
    else:
        return "Não há quartos disponíveis para check-in."