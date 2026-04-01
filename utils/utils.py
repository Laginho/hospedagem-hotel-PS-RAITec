import os



# Códigos ANSI para cores no terminal
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
AZUL = '\033[94m'
NEGRITO = '\033[1m'
RESET = '\033[0m'


def limpar_tela():
    # O os.name == 'nt' verifica se é Windows. Se for, roda 'cls', senão roda 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar_tela():
    input("\nPressione Enter para continuar...")


