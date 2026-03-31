"""Módulo de auxiliar para funções relacionadas às reservas de quartos do hotel.

"""

from helper_db import parse_csv

def print_quartos_disponiveis():
    """Imprime os quartos disponíveis formatados como uma tabela."""
    
    data = parse_csv("quartos.csv")
    
    for quarto in data:
        if quarto["DISPONIBILIDADE"].strip().upper() == "DISPONÍVEL":
            print(f"Quarto {quarto['QUARTO']} - Disponível")
    
print_quartos_disponiveis()