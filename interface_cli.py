from helper_quartos import print_quartos_disponiveis, fazer_checkin, consultar_reserva, cancelar_reserva
from validacoes import ler_texto_obrigatorio, tem_quarto_disponivel
from utils.utils import limpar_tela, pausar_tela, AMARELO, RESET, VERMELHO


def menu_cliente_cli():

    while True:
        limpar_tela()

        print("\n" + "="*35)
        print(" "*9 + "ÁREA DO CLIENTE")
        print("="*35 + "\n")


        print(" > [1] - Ver quartos disponíveis")
        print(" > [2] - Fazer uma reserva (Check-in)")
        print(" > [3] - Consultar minhas reserva")
        print(" > [4] - Cancelar minha reserva")
        print(" > [0] - Sair")
        print("\n" + "-" * 35)

        opcao = input("\n >> Escolha uma opção: ").strip()
        print("\n\n")

        if opcao == "1":

            print_quartos_disponiveis()
            pausar_tela()

        elif opcao == "2":

            if not tem_quarto_disponivel():
                print(f"\n{VERMELHO} Desculpe, o hotel está com 100% de ocupação no momento.{RESET}")
                pausar_tela()
                continue

            nome = ler_texto_obrigatorio("Digite seu nome para a reserva: ")
            print_quartos_disponiveis()
            quarto = input("Digite o número do quarto desejado: ").strip()
            dias = input("Digite a quantidade de dias para a reserva: ").strip()
            print(fazer_checkin(nome, quarto, dias))
            pausar_tela()

        elif opcao == "3":
            nome = input("Digite seu nome para consultar as reservas: ").strip()
            print(consultar_reserva(nome))
            pausar_tela()
        elif opcao == "4":
            nome = input("Digite seu nome para cancelar a reserva: ").strip()
            print(consultar_reserva(nome))
            quarto = input("Digite o número do quarto que deseja cancelar: ").strip()
            print(cancelar_reserva(nome, quarto))
            pausar_tela()
        elif opcao == "0":
            print("\nFinalizando Programa...")
            exit()
        else:
            print("ERRO: Digite uma opção válida!")
            pausar_tela()


def menu_funcionario_cli():

    senha = input("Digite a senha de acesso: ").strip()

    if senha == "raiteis2026":
        print("\nAcesso Liberado!")
        pausar_tela()

        while True:
            limpar_tela()

            print("\n" + "="*35)
            print(" "*3 + "ÁREA DO FUNCIONÁRIO")
            print("="*35 + "\n")

            print(" > [1] - Cadastrar Cliente")
            print(" > [2] - Gerenciar Quartos")
            print(" > [3] - Registrar Checkout")
            print(" > [4] - Visualizar Base de Dados")
            print(" > [0] - Sair")
            print("\n" + "-"*35)

            opcao = input("\n >> Escolha uma opção: ").strip()

            if opcao == "1":
                print("Cadastrar Cliente")
            elif opcao == "2":
                print("Gerenciar Quartos")
            elif opcao == "3":
                print("Registrar Checkout")
            elif opcao == "4":
                print("Visualizar Base de Dados")
            elif opcao == "0":
                print("Finalizando Programa...")
                exit()
            else:
                print("ERRO: Digite uma opção válida!")
                pausar_tela()

    else: 
        print("Senha Incorreta! Acesso Negado!")

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
            menu_cliente_cli()
        elif opcao == "2":
            menu_funcionario_cli()
        elif opcao == "0":
            print("Finalizando Programa...")
            break
        else:
            print("ERRO: Digite uma opção válida!")
            pausar_tela()