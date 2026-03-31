from helper_quartos import print_quartos_disponiveis

def menu_cliente_cli():

    while True:

        print("\n" + "="*35)
        print("Área do Cliente")
        print("="*35)

        print("1 - Ver quartos disponíveis")
        print("2 - Fazer uma reserva (Check-in)")
        print("3 - Consultar minha reserva")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()
        print("\n\n")

        if opcao == "1":
            print_quartos_disponiveis()
        elif opcao == "2":
            print("FUNÇÃO DE CHECKIN")
        elif opcao == "3":
            print("CONSULTAR RESERVA")
        elif opcao == "0":
            print("\nFinalizando Programa...")
            break
        else:
            print("ERRO: Digite uma opção válida!")


def menu_funcionario_cli():

    senha = input("Digite a senha de acesso: ").strip()

    if senha == "raiteis2026":
        print("\nAcesso Liberado!")

        while True:

            print("\n" + "="*35)
            print("Área do Funcionário")
            print("="*35)

            print("1 - Cadastrar Cliente")
            print("2 - Gerenciar Quartos")
            print("3 - Registrar Checkout")
            print("4 - Visualizar Base de Dados")
            print("0 - Sair")
            print("-"*35)

            opcao = input("Escolha uma opção: ").strip()

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
                break
            else:
                print("ERRO: Digite uma opção válida!")

    else: 
        print("Senha Incorreta! Acesso Negado!")

def menu_principal():

    while True:

        print("\n" + "="*35)
        print("SISTEMA DE HOSPEDAGEM RAITEIS")
        print("="*35)

        print("1 - Acesso Cliente")
        print("2 - Acesso Funcionário")
        print("0 - Sair")
        print("-"*35)

        opcao = input("Escolha o seu perfil de acesso: ").strip()

        if opcao == "1":
            menu_cliente_cli()
        elif opcao == "2":
            menu_funcionario_cli()
        elif opcao == "0":
            print("Finalizando Programa...")
            break
        else:
            print("ERRO: Digite uma opção válida!")