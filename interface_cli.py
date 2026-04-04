from helper_cli import *


#==================================================================================================================
#==================================================================================================================



def menu_cliente_cli(usuario_atual):                                # MENU DO CLIENTE: Tudo que o cliente pode acessar.

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

        if opcao == "1":

            limpar_tela()
            print_quartos_disponiveis()
            pausar_tela()

        elif opcao == "2":

            fluxo_fazer_reserva(usuario_atual)

        elif opcao == "3":

            limpar_tela()
            nome = usuario_atual.getNome()
            print(consultar_reserva(nome))
            pausar_tela()

        elif opcao == "4":

            limpar_tela()
            nome = usuario_atual.getNome()
            print(consultar_reserva(nome))
            quarto = input("Digite o número do quarto que deseja cancelar: ").strip()
            print(cancelar_reserva(nome, quarto))
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

    while True:
        limpar_tela()

        print("\n" + "="*35)
        print(" "*3 + "ÁREA DO FUNCIONÁRIO")
        print("="*35 + "\n")

        print(" > [1] - Cadastrar Cliente")
        print(" > [2] - Gerenciar Quartos")
        print(" > [3] - Registrar Checkout")
        print(" > [4] - Visualizar Base de Dados")
        print(" > [5] - Cadastrar Funcionário")
        print(" > [0] - Sair")
        print("\n" + "-"*35)

        opcao = input("\n >> Escolha uma opção: ").strip()

        if opcao == "1":

            sucesso = fluxo_de_cadastro("Cliente")

            if sucesso:
                print(f"\n{VERDE}Novo cliente cadastrado com sucesso!{RESET}")

            pausar_tela()

        elif opcao == "2":

            menu_gerenciar_quartos()

        elif opcao == "3":
            print("Registrar Checkout")
        elif opcao == "4":
            print("Visualizar Base de Dados")

        elif opcao == "5":

            sucesso = fluxo_de_cadastro("Funcionário")

            if sucesso:
                print(f"\n{VERDE}Novo funcionário cadastrado com sucesso!{RESET}")

            pausar_tela()


        elif opcao == "0":
            print(f"\n{AZUL}Finalizando Programa...{RESET}")
            exit()
        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================



def menu_gerenciar_quartos():

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
            print("Fluxo de Manutenção...")
            pausar_tela()
        elif opcao == "4":
            print("Fluxo de Excluir Quarto...")
            pausar_tela()
        elif opcao == "0":
            break  
        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()


#==================================================================================================================
#==================================================================================================================



def menu_portal_cliente():
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