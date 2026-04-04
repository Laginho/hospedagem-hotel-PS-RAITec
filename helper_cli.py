from validacoes import *
from helper_db import cadastrar_usuario_bd, autenticar_usuario_db
from utils.utils import pausar_tela, limpar_tela
from classes_raiteis import Cliente, Funcionario
from helper_quartos import *


#==================================================================================================================
#==================================================================================================================


def fluxo_de_cadastro(tipo_usuario):
    print(f"\n--- NOVO CADASTRO DE {tipo_usuario.upper()} ---")
    nome = ler_texto_obrigatorio(f"  >> Digite o Nome Completo do {tipo_usuario}: ")

    cancelou_cadastro = False

    while True:
        cpf = ler_cpf("  >> Digite o CPF (apenas números): ")

        if cpf_ja_cadastrado(cpf):
            print(f"\n{VERMELHO}ERRO: Este CPF já possui uma conta no sistema!{RESET}")
            print(f"{AMARELO}Você pode tentar outro CPF ou cancelar a operação.{RESET}")
            escolha = input("  >> Digite [0] para cancelar ou [Enter] para tentar outro: ").strip()

            if escolha == "0":
                cancelou_cadastro = True
                break
            else:
                continue
        else:
            break

    if cancelou_cadastro:
        return False

    senha = ler_texto_obrigatorio("  >> Crie uma senha: ")

    cadastrar_usuario_bd(tipo_usuario, nome, cpf, senha)

    return True


#==================================================================================================================
#==================================================================================================================


def fluxo_de_login(tipo_usuario):
    """Gerencia as telas de input de login e retorna o objeto do usuário logado."""
    print(f"\n--- LOGIN DE {tipo_usuario.upper()} ---")

    while True:
        cpf_digitado = ler_cpf("  >> Digite seu CPF (apenas números) ou [0] para cancelar: ")

        if cpf_digitado == "0":
            return None

        senha_digitada = ler_texto_obrigatorio("  >> Digite sua senha: ")

        conta_encontrada = autenticar_usuario_db(cpf_digitado, senha_digitada, tipo_usuario)

        if conta_encontrada:
            print(f"\n{VERDE}Login efetuado com sucesso! Bem-vindo(a), {conta_encontrada['NOME']}.{RESET}")
            pausar_tela()

            if tipo_usuario == "Cliente":
                return Cliente(nome=conta_encontrada["NOME"], cpf=conta_encontrada["USUARIO"])
            elif tipo_usuario == "Funcionário":
                return Funcionario(nome=conta_encontrada["NOME"], cpf=conta_encontrada["USUARIO"],
                                   senha=conta_encontrada["SENHA"])

        else:
            print(f"\n{VERMELHO}ERRO: CPF não encontrado ou senha incorreta.{RESET}")
            print(f"{AMARELO}Tente novamente ou digite [0] para voltar.{RESET}\n")


#==================================================================================================================
#==================================================================================================================


def fluxo_fazer_reserva(cliente):
    limpar_tela()

    if not tem_quarto_disponivel():
        print(f"\n{VERMELHO}Desculpe, o hotel está com 100% de ocupação no momento.{RESET}")
        pausar_tela()
        return

    print_quartos_disponiveis()
    quarto = ler_texto_obrigatorio("Digite o número do quarto desejado: ").strip()

    if not quarto_esta_livre(quarto):
        print(f"\n{VERMELHO}ERRO: O quarto {quarto} não existe ou já está reservado!{RESET}")
        pausar_tela()
        return

    data_checkin = ler_data_futura("Digite a data do Check-in (DD/MM/AAAA): ")
    dias = input("Digite a quantidade de dias para a reserva: ").strip()

    mensagem_sucesso = fazer_checkin(cliente.getNome(), quarto, dias, data_checkin)

    print(f"\n{mensagem_sucesso}")
    pausar_tela()


#==================================================================================================================
#==================================================================================================================


def fluxo_adicionar_quarto():
    """Gerencia a tela de criação de um novo quarto."""
    limpar_tela()
    print("\n" + "=" * 35)
    print(" " * 7 + "ADICIONAR NOVO QUARTO")
    print("=" * 35 + "\n")

    print_todos_os_quartos()

    while True:
        numero = ler_texto_obrigatorio("\n  >> Digite o número do novo quarto (ou [0] para cancelar): ").strip()

        if numero == "0":
            return

        try:

            preco = float(input("  >> Digite o valor da diária (ex: 150.00): ").strip())

            if preco < 0:
                print(f"{VERMELHO}ERRO: O preço da diária não pode ser negativo.{RESET}")
                continue

        except ValueError:
            print(f"{VERMELHO}ERRO: Digite um valor numérico válido para o preço (use ponto para os centavos).{RESET}")
            continue


        sucesso = adicionar_quarto_db(numero, preco)

        if sucesso:
            print(f"\n{VERDE}Sucesso! Quarto {numero} adicionado com diária de R$ {preco:.2f}.{RESET}")
            pausar_tela()
            break
        else:
            print(f"\n{VERMELHO}ERRO: O quarto {numero} já existe no sistema!{RESET}")
            print(f"{AMARELO}Tente outro número.{RESET}")


#==================================================================================================================
#==================================================================================================================


def fluxo_alterar_preco():
    """Gerencia a tela de alteração do valor da diária de um quarto."""
    limpar_tela()
    print("\n" + "=" * 35)
    print(" " * 4 + "ALTERAR PREÇO DA DIÁRIA")
    print("=" * 35 + "\n")

    print_todos_os_quartos()

    while True:
        numero = ler_texto_obrigatorio("\n  >> Digite o número do quarto (ou [0] para cancelar): ").strip()

        if numero == "0":
            return


        status = verificar_status_quarto(numero)

        if status == "NAO_ENCONTRADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} não existe no sistema!{RESET}")
            continue

        elif status != "DISPONÍVEL":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} está {status}!{RESET}")
            print(f"{AMARELO}Não é permitido alterar o preço de um quarto ocupado ou em manutenção.{RESET}")
            continue
        # ------------------------------


        try:
            novo_preco = float(input("  >> Digite o NOVO valor da diária (ex: 180.00): ").strip())

            if novo_preco < 0:
                print(f"{VERMELHO}ERRO: O preço da diária não pode ser negativo.{RESET}")
                continue

        except ValueError:
            print(f"{VERMELHO}ERRO: Digite um valor numérico válido (use ponto para os centavos).{RESET}")
            continue


        alterar_preco_quarto_db(numero, novo_preco)
        print(f"\n{VERDE}Sucesso! A diária do quarto {numero} foi atualizada para R$ {novo_preco:.2f}.{RESET}")
        pausar_tela()
        break