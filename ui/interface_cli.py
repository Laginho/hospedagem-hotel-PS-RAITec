"""Menus principais da interface de linha de comando do sistema.

Este módulo define a navegação entre portais de cliente e funcionário,
delegando ações operacionais para os fluxos implementados na camada helper.
"""

from services.helper_quartos import cancelar_reserva, consultar_reserva, print_quartos_disponiveis
from ui.helper_cli import (
    fluxo_adicionar_quarto,
    fluxo_alterar_preco,
    fluxo_de_cadastro,
    fluxo_de_login,
    fluxo_excluir_quarto,
    fluxo_fazer_reserva,
    fluxo_fazer_reserva_funcionario,
    fluxo_manutencao_quarto,
    fluxo_registrar_checkout,
    fluxo_visualizar_base,
)
from utils.utils import AZUL, RESET, VERDE, VERMELHO, limpar_tela, pausar_tela


#==================================================================================================================
#==================================================================================================================



def menu_cliente_cli(usuario_atual):                                # MENU DO CLIENTE: Tudo que o cliente pode acessar.
    """Exibe e controla o menu da área do cliente.

    Args:
        usuario_atual: Objeto do cliente autenticado no sistema.

    O menu permite consultar disponibilidade, reservar, consultar reservas e
    cancelar reservas do próprio usuário.
    """

    while True:
        limpar_tela()                                  # A função limpar_tela é puramente estética, rode o programa no console "Alt + F12" -> Python main.py

        print("\n" + "="*35)
        print(" "*9 + "ÁREA DO CLIENTE")
        print("="*35 + "\n")


        print(" > [1] - Ver quartos disponíveis")
        print(" > [2] - Fazer uma reserva (Check-in)")
        print(" > [3] - Consultar minhas reservas")
        print(" > [4] - Cancelar minha reserva")
        print(" > [0] - Sair")
        print("\n" + "-" * 35)

        opcao = input("\n >> Escolha uma opção: ").strip()
        print("\n\n")

        nome = usuario_atual.getNome()   #alterei isso para que ele pudesse pegar os dados antes, já que repetia muito durante os if s
        cpf = usuario_atual.getCPF()    #pegar o cpf pra poder usar os métodos helper enviando ele também

        if opcao == "1":

            limpar_tela()
            print_quartos_disponiveis()
            pausar_tela()

        elif opcao == "2":

            fluxo_fazer_reserva(usuario_atual)

        elif opcao == "3":

            limpar_tela()
            print(consultar_reserva(nome,cpf))
            pausar_tela()

        elif opcao == "4":

            limpar_tela()
            print(consultar_reserva(nome,cpf))
            quarto = input("Digite o número do quarto que deseja cancelar: ").strip()
            print(cancelar_reserva(nome, cpf, quarto))
            pausar_tela()

        elif opcao == "0":
            limpar_tela()
            print(f"\n{AZUL}Finalizando Programa...{RESET}")
            exit()

        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================

def menu_funcionario_cli():                             # MENU DO FUNCIONÁRIO: Tudo que o funcionário pode acessar.
    """Exibe e controla o menu principal da área de funcionário.

    O menu centraliza operações de balcão, cadastro e administração de quartos
    e bases de dados.
    """

    while True:
        limpar_tela()

        print("\n" + "="*35)
        print(" "*3 + "ÁREA DO FUNCIONÁRIO")
        print("="*35 + "\n")

        print(" > [1] - Nova Reserva (Balcão)")
        print(" > [2] - Cadastrar Cliente")
        print(" > [3] - Registrar Checkout")
        print(" > [4] - Gerenciar Quartos")
        print(" > [5] - Visualizar Base de Dados")
        print(" > [6] - Cadastrar Funcionário")
        print(" > [0] - Sair")
        print("\n" + "-"*35)

        opcao = input("\n >> Escolha uma opção: ").strip()

        if opcao == "1":

            fluxo_fazer_reserva_funcionario()

        elif opcao == "2":


            sucesso = fluxo_de_cadastro("Cliente")

            if sucesso:
                print(f"\n{VERDE}Novo cliente cadastrado com sucesso!{RESET}")

            pausar_tela()


        elif opcao == "3":

            fluxo_registrar_checkout()

        elif opcao == "4":

            menu_gerenciar_quartos()

        elif opcao == "5":

            fluxo_visualizar_base()

        elif opcao == "6":

            sucesso = fluxo_de_cadastro("Funcionário")

            if sucesso:
                print(f"\n{VERDE}Novo funcionário cadastrado com sucesso!{RESET}")

            pausar_tela()


        elif opcao == "0":
            print(f"\n{AZUL}Fazendo logoff...{RESET}")
            break
            
        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================



def menu_gerenciar_quartos():
    """Exibe submenu de gerenciamento de quartos para funcionários.

    Reúne operações de criação, atualização de preço, manutenção e exclusão de
    quartos.
    """

    while True:
        limpar_tela()
        print("\n" + "=" * 35)
        print(" " * 5 + "GERENCIAR QUARTOS")
        print("=" * 35 + "\n")

        print(" > [1] - Adicionar Novo Quarto")
        print(" > [2] - Alterar Preço da Diária")
        print(" > [3] - Colocar/Tirar de Manutenção")
        print(" > [4] - Excluir Quarto")
        print(" > [0] - Voltar")
        print("\n" + "-" * 35)

        opcao = input("\n >> Escolha uma opção: ").strip()

        if opcao == "1":

            fluxo_adicionar_quarto()

        elif opcao == "2":

            fluxo_alterar_preco()

        elif opcao == "3":

            fluxo_manutencao_quarto()

        elif opcao == "4":

            fluxo_excluir_quarto()

        elif opcao == "0":
            break
        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================



def menu_portal_cliente():
    """Exibe o portal de entrada do cliente."""
    while True:
        limpar_tela()
        print("\n" + "="*35)
        print("         PORTAL DO CLIENTE")
        print("="*35 + "\n")
        print("  > [1] Já sou cliente (Fazer Login)")
        print("  > [2] Quero criar minha conta")
        print("  > [0] Voltar ao Menu Principal")
        print("\n" + "-"*35)

        opcao = input("\n  >> Escolha uma opção: ").strip()

        if opcao == '1':

            cliente_logado = fluxo_de_login("Cliente")

            if cliente_logado:
                menu_cliente_cli(cliente_logado)

        elif opcao == '2':

            sucesso = fluxo_de_cadastro("Cliente")

            if sucesso:
                print(f"\n{VERDE}Conta de Cliente criada com sucesso!{RESET}")

            pausar_tela()

        elif opcao == '0':
            break

        else:
            print(f"\n{VERMELHO}Opção inválida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================


def menu_portal_funcionario():
    """Exibe o portal de entrada do funcionário.

    O acesso é feito por login antes de liberar o menu administrativo.
    """
    while True:
        limpar_tela()
        print("\n" + "="*35)
        print("       PORTAL DO FUNCIONÁRIO")
        print("="*35 + "\n")
        print("  > [1] Fazer Login")
        print("  > [0] Voltar ao Menu Principal")
        print("\n" + "-"*35)

        opcao = input("\n  >> Escolha uma opção: ").strip()

        if opcao == '1':

            funcionario_logado = fluxo_de_login("Funcionário")

            if funcionario_logado:
                menu_funcionario_cli()

        elif opcao == '0':
            break

        else:
            print(f"\n{VERMELHO}Opção inválida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================


def menu_principal():
    """Renderiza o menu principal e roteia para cada portal de acesso.

    Este é o ponto central de navegação do programa em execução no terminal.
    """

    while True:
        limpar_tela()

        print("\n" + "="*35)
        print(" "*3 + "SISTEMA DE HOSPEDAGEM RAITEIS")
        print("="*35 + "\n")

        print(" > [1] - Acesso Cliente")
        print(" > [2] - Acesso Funcionário")
        print(" > [0] - Sair")
        print("\n" + "-"*35)

        opcao = input("\n >> Escolha o seu perfil de acesso: ").strip()

        if opcao == "1":
            menu_portal_cliente()
        elif opcao == "2":
            menu_portal_funcionario()
        elif opcao == "0":
            print(f"\n{AZUL}Finalizando Programa...{RESET}")
            break
        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()