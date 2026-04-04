from validacoes import *
from helper_db import cadastrar_usuario_bd, autenticar_usuario_db
from utils.utils import VERMELHO, VERDE, AMARELO, RESET, pausar_tela, limpar_tela
from classes_raiteis import Cliente, Funcionario
from helper_quartos import print_quartos_disponiveis, fazer_checkin

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