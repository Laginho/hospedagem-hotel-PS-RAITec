from helper_quartos import print_quartos_disponiveis, fazer_checkin, consultar_reserva, cancelar_reserva
from validacoes import ler_texto_obrigatorio, tem_quarto_disponivel, quarto_esta_livre, ler_data_futura, validar_login, get_nome_cliente, ler_cpf, cpf_ja_cadastrado
from helper_db import parse_csv, save_csv
from utils.utils import limpar_tela, pausar_tela, AMARELO, RESET, VERMELHO, VERDE, AZUL
from classes_raiteis import Funcionario, Cliente


#==================================================================================================================
#==================================================================================================================


# --- MOCK DE DADOS PARA TESTAR A INTEGRAÇÃO ---
funcionarios_cadastrados = [
    # Criando um funcionário admin de teste
    Funcionario(nome="Admin Teste", cpf="00011122233", senha="admin")
]
clientes_cadastrados = [] # Lista que vai guardar os clientes que forem cadastrados
# ----------------------------------------------


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

            limpar_tela()

            if not tem_quarto_disponivel():                                         # Essa função verifica a existência de quartos disponíveis para prosseguir com a reserva.

                print(f"\n{VERMELHO} Desculpe, o hotel está com 100% de ocupação no momento.{RESET}")
                pausar_tela()
                continue

            nome = usuario_atual.getNome()        # Esse input não vai ser útil quando o login do cliente for implementado
            print_quartos_disponiveis()
            quarto = ler_texto_obrigatorio("Digite o número do quarto desejado: ").strip()

            if not quarto_esta_livre(quarto):                                       # Função para verificar se o quarto escolhido está disponível para reserva.

                print(f"\n{VERMELHO}ERRO: O quarto {quarto} não existe ou já está reservado!{RESET}")
                pausar_tela()
                continue

            data_checkin = ler_data_futura("Digite a data do Check-in (DD/MM/AAAA): ")
            dias = input("Digite a quantidade de dias para a reserva: ").strip()
            print(fazer_checkin(nome, quarto, dias, data_checkin))
            pausar_tela()

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
            print(f"\n{AZUL}Finalizando Programa...{RESET}")
            exit()
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
            print("\n--- LOGIN DE CLIENTE ---")
            cpf_digitado = ler_cpf("  >> Digite seu CPF (apenas números): ")
            senha_digitada = ler_texto_obrigatorio("  >> Digite sua senha: ")

            # Procura o cliente na lista
            if validar_login(cpf_digitado, senha_digitada):
                nome = get_nome_cliente(cpf_digitado)
                print(f"\n{VERDE}Login efetuado! Bem-vindo(a) de volta, {nome}.{RESET}")
                pausar_tela()
                cliente_logado = Cliente(nome=nome, cpf=cpf_digitado)
                menu_cliente_cli(cliente_logado)
            else:
                print(f"\n{VERMELHO}ERRO: não foi possível autenticar. Por favor, confira se os dados estão corretos e tente novamente.{RESET}")
                pausar_tela()

        elif opcao == '2':
            print("\n--- NOVO CADASTRO ---")
            nome = ler_texto_obrigatorio("  >> Digite seu Nome Completo: ")

            while True:
                cpf = ler_cpf("  >> Digite seu CPF (apenas números): ")

                if cpf_ja_cadastrado(cpf):
                    print(f"\n{VERMELHO}ERRO: Este CPF já possui uma conta no sistema!{RESET}")

                    # A ROTA DE FUGA ENTRA AQUI:
                    print(f"{AMARELO}Você pode tentar outro CPF ou voltar para fazer Login.{RESET}")
                    escolha = input("  >> Digite [0] para voltar ou [Enter] para tentar outro CPF: ").strip()

                    if escolha == "0":
                        cancelou_cadastro = True  # Levanta a bandeira de desistência
                        break  # Quebra o loop do CPF
                    else:
                        continue  # Reinicia o loop do CPF pra ele tentar de novo
                else:
                    # Se não tá cadastrado, quebra o loop e prossegue com o cadastro
                    break

            if cancelou_cadastro:
                continue

            senha = ler_texto_obrigatorio("  >> Crie uma senha para sua conta: ")

            novo_cliente = Cliente(nome=nome, cpf=cpf)
            clientes_cadastrados.append(novo_cliente)
            save_csv("credenciais.csv", [{"TIPO": "Cliente", "USUARIO": cpf, "SENHA": senha, "NOME": nome}])

            print(f"\n{VERDE}Conta criada com sucesso! Objeto Cliente gerado na memória e credenciais salvas no banco de dados.{RESET}")
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
            if opcao == '1':
                print("\n--- LOGIN DA ADMINISTRAÇÃO ---\n")

                cpf_digitado = ler_texto_obrigatorio("  >> Digite seu CPF (apenas números): ")

                senha_digitada = ler_texto_obrigatorio("  >> Digite sua senha: ")


                funcionario_logado = None                   # Busca se o CPF digitado existe na lista mock de funcionários
                for func in funcionarios_cadastrados:
                    if func.cpf == cpf_digitado:
                        funcionario_logado = func
                        break

                if funcionario_logado:
                    if funcionario_logado.validar_login(senha_digitada):
                        print(f"\n{VERDE}Acesso liberado! Bem-vindo(a), {funcionario_logado.nome}.{RESET}")
                        pausar_tela()
                        menu_funcionario_cli()
                    else:
                        print(f"\n{VERMELHO}ERRO: Senha incorreta!{RESET}")
                        pausar_tela()
                else:
                    print(f"\n{VERMELHO}ERRO: CPF não encontrado no sistema.{RESET}")
                    pausar_tela()

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