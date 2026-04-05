
"""Fluxos de interação do terminal para cadastro, login e operações de hotel.

Este módulo concentra as rotinas da camada CLI que orquestram validações,
serviços e mensagens ao usuário para operações de cliente e funcionário.
"""

from datetime import date, datetime

from models.classes_raiteis import Cliente, Funcionario
from services.helper_db import (
    autenticar_usuario_db,
    buscar_nome_cliente_por_cpf,
    cadastrar_usuario_bd,
    parse_csv,
)
from services.helper_quartos import (
    adicionar_quarto_db,
    alterar_preco_quarto_db,
    alterar_status_quarto_db,
    excluir_quarto_db,
    fazer_checkin,
    liberar_quarto_db,
    obter_quarto_db,
    print_quartos_disponiveis,
    print_todos_os_quartos,
    verificar_status_quarto,
)
from utils.utils import AMARELO, AZUL, RESET, VERDE, VERMELHO, limpar_tela, pausar_tela
from utils.validacoes import (
    cpf_ja_cadastrado,
    ler_cpf,
    ler_data_futura,
    ler_data_nascimento,
    ler_endereco,
    ler_texto_obrigatorio,
    quarto_esta_livre,
    tem_quarto_disponivel,
)

#==================================================================================================================
#==================================================================================================================


def fluxo_de_cadastro(tipo_usuario):
    """Executa o fluxo de cadastro de clientes ou funcionários.

    Args:
        tipo_usuario: Perfil a ser cadastrado, como Cliente ou Funcionário.

    Returns:
        bool: True quando o cadastro é concluído; False quando o usuário
            cancela a operação.
    """
    print(f"\n--- NOVO CADASTRO DE {tipo_usuario.upper()} ---")
    nome = ler_texto_obrigatorio(f"  >> Digite o Nome Completo do {tipo_usuario}: ")

    if tipo_usuario == "Cliente":
        nascimento = ler_data_nascimento("  >> Digite a Data de Nascimento (DD/MM/AAAA): ")
        endereco = ler_endereco("  >> Digite a Cidade/Estado (Ex: Fortaleza - CE): ")
    else:
        # Se for funcionário, o sistema preenche sozinho pra não quebrar o CSV
        nascimento = "N/A"
        endereco = "N/A"

    cancelou_cadastro = False

    while True:
        cpf = ler_cpf("  >> Digite o CPF (apenas números) ou [0] para cancelar: ")

        if cpf == "0":
            cancelou_cadastro = True
            break

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

    cadastrar_usuario_bd(tipo_usuario, nome, cpf, senha, nascimento, endereco)

    return True


#==================================================================================================================
#==================================================================================================================


def fluxo_de_login(tipo_usuario):
    """Executa o fluxo de login e retorna o usuário autenticado.

    Args:
        tipo_usuario: Perfil esperado para autenticação.

    Returns:
        Cliente | Funcionario | None: Objeto de domínio do usuário autenticado
            ou None quando o login é cancelado.
    """
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
                return Cliente(nome=conta_encontrada["NOME"], cpf=conta_encontrada["USUARIO"], senha=conta_encontrada["SENHA"])
            elif tipo_usuario == "Funcionário":
                return Funcionario(nome=conta_encontrada["NOME"], cpf=conta_encontrada["USUARIO"],
                                   senha=conta_encontrada["SENHA"])

        else:
            print(f"\n{VERMELHO}ERRO: CPF não encontrado ou senha incorreta.{RESET}")
            print(f"{AMARELO}Tente novamente ou digite [0] para voltar.{RESET}\n")


#==================================================================================================================
#==================================================================================================================


def fluxo_fazer_reserva(cliente):
    """Conduz o fluxo de reserva para um cliente já autenticado.

    Args:
        cliente: Instância de cliente com dados de nome e CPF.

    O fluxo valida disponibilidade geral e disponibilidade específica do quarto
    antes de efetivar o check-in.
    """
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

    mensagem_sucesso = fazer_checkin(cliente.getNome(), cliente.getCPF(), quarto, dias, data_checkin)
    # alterado pra receber cpf

    print(f"\n{mensagem_sucesso}")
    pausar_tela()


#==================================================================================================================
#==================================================================================================================


def fluxo_adicionar_quarto():
    """Gerencia o fluxo de criação de um novo quarto.

    A função valida preço e evita cadastro duplicado de número de quarto.
    """
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
    """Gerencia o fluxo de alteração da diária de um quarto.

    Apenas quartos disponíveis podem ter a diária alterada.
    """
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

#==================================================================================================================
#==================================================================================================================

def fluxo_manutencao_quarto():
    """Alterna o status de um quarto entre DISPONÍVEL e MANUTENÇÃO.

    Quartos reservados não podem entrar em manutenção.
    """
    limpar_tela()
    print("\n" + "=" * 35)
    print(" " * 4 + "MANUTENÇÃO DE QUARTOS")
    print("=" * 35 + "\n")

    print_todos_os_quartos()

    while True:
        numero = ler_texto_obrigatorio("\n  >> Digite o número do quarto (ou [0] para cancelar): ").strip()

        if numero == "0":
            return


        status_atual = verificar_status_quarto(numero)

        if status_atual == "NAO_ENCONTRADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} não existe no sistema!{RESET}")
            continue

        elif status_atual == "RESERVADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} está Reservado!{RESET}")
            print(
                f"{AMARELO}Você não pode colocar um quarto em manutenção enquanto houver reservas ativas nele.{RESET}")
            continue

        elif status_atual == "DISPONÍVEL":
            novo_status = "MANUTENÇÃO"
            mensagem_sucesso = f"colocado em {AMARELO}MANUTENÇÃO{RESET}"

        elif status_atual == "MANUTENÇÃO":
            novo_status = "DISPONÍVEL"
            mensagem_sucesso = f"liberado e agora está {VERDE}DISPONÍVEL{RESET}"
        # ------------------------------------

        # Manda salvar o novo status
        alterar_status_quarto_db(numero, novo_status)

        print(f"\n{VERDE}Sucesso! O quarto {numero} foi {mensagem_sucesso}.{RESET}")
        pausar_tela()
        break

#==================================================================================================================
#==================================================================================================================

def fluxo_excluir_quarto():
    """Gerencia o fluxo de exclusão definitiva de um quarto.

    A exclusão exige confirmação explícita e é bloqueada para quartos
    reservados.
    """
    limpar_tela()
    print("\n" + "=" * 35)
    print(" " * 10 + "EXCLUIR QUARTO")
    print("=" * 35 + "\n")

    print_todos_os_quartos()

    while True:
        numero = ler_texto_obrigatorio("\n  >> Digite o número do quarto para EXCLUIR (ou [0] para cancelar): ").strip()

        if numero == "0":
            return

        status_atual = verificar_status_quarto(numero)

        if status_atual == "NAO_ENCONTRADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} não existe no sistema!{RESET}")
            continue

        elif status_atual == "RESERVADO":
            print(f"\n{VERMELHO}ERRO: Operação bloqueada!{RESET}")
            print(
                f"{AMARELO}O quarto {numero} está com um hóspede no momento. Aguarde o check-out para excluí-lo.{RESET}")
            continue
        # ---------------------------------------------

        # Se chegou aqui, o quarto existe e está vazio (DISPONÍVEL ou MANUTENÇÃO).
        print(f"\n{AMARELO}ATENÇÃO: Você está prestes a excluir o quarto {numero} permanentemente!{RESET}")
        confirmacao = input(
            "  >> Digite 'SIM' para confirmar a exclusão ou qualquer outra coisa para cancelar: ").strip().upper()

        if confirmacao == 'SIM':
            excluir_quarto_db(numero)
            print(f"\n{VERDE}Sucesso! O quarto {numero} foi removido do sistema.{RESET}")
            pausar_tela()
            break
        else:
            print(f"\n{AZUL}Operação cancelada. O quarto não foi excluído.{RESET}")
            pausar_tela()
            break

#==================================================================================================================
#==================================================================================================================

def fluxo_registrar_checkout():
    """Gerencia o checkout, cálculo da conta e liberação do quarto.

    O fluxo só prossegue para quartos reservados e pode aplicar cobrança
    mínima de uma diária quando o período calculado for zero.
    """
    limpar_tela()
    print("\n" + "=" * 35)
    print(" " * 8 + "REGISTRAR CHECKOUT")
    print("=" * 35 + "\n")

    print_todos_os_quartos()

    while True:
        numero = ler_texto_obrigatorio(
            "\n  >> Digite o número do quarto para Checkout (ou [0] para cancelar): ").strip()

        if numero == "0":
            return

            # --- A NOSSA BARREIRA ---
        status = verificar_status_quarto(numero)

        if status == "NAO_ENCONTRADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} não existe!{RESET}")
            continue

        elif status != "RESERVADO":
            print(f"\n{VERMELHO}ERRO: O quarto {numero} não está ocupado!{RESET}")
            print(f"{AMARELO}Só é possível fazer checkout de quartos com status RESERVADO.{RESET}")
            continue
        # ------------------------

        # Se chegou aqui, tem hóspede! Vamos calcular a conta.
        quarto = obter_quarto_db(numero)
        cliente = quarto["CLIENTE"]

        data_in = date.fromisoformat(quarto["CHECKIN"])
        data_out = date.fromisoformat(quarto["CHECKOUT"])
        dias_hospedados = (data_out - data_in).days

        # Prevenção: Se o cliente fez check-in e check-out no mesmo dia, cobramos 1 diária no mínimo.
        if dias_hospedados == 0:
            dias_hospedados = 1

        valor_diaria = float(quarto.get("DIARIA", "0") or "0")
        valor_total = valor_diaria * dias_hospedados

        print("\n--- RESUMO DA CONTA ---")
        print(f" Hóspede: {cliente}")
        print(f" Período: {quarto['CHECKIN']} até {quarto['CHECKOUT']} ({dias_hospedados} diárias)")
        print(f" Valor Total: {VERDE}R$ {valor_total:.2f}{RESET}")
        print("-" * 23)

        confirmacao = input("\n  >> O pagamento foi realizado? Digite 'SIM' para liberar o quarto: ").strip().upper()

        if confirmacao == "SIM":
            liberar_quarto_db(numero)
            print(f"\n{VERDE}Checkout concluído com sucesso! O quarto {numero} está livre novamente.{RESET}")
            pausar_tela()
            break
        else:
            print(f"\n{AZUL}Operação cancelada. O quarto continua reservado.{RESET}")
            pausar_tela()
            break



#==================================================================================================================
#==================================================================================================================


def print_todos_os_usuarios():
    """Exibe a base de usuários em tabelas separadas por perfil.

    Funcionários são exibidos em tabela simplificada e clientes em tabela com
    campos adicionais para análise (idade e endereço).
    """
    data = parse_csv("data/credenciais.csv")

    funcionarios = [c for c in data if c.get("TIPO") == "Funcionário"]
    clientes = [c for c in data if c.get("TIPO") == "Cliente"]

    # Função interna rápida para calcular a idade
    def calcular_idade(data_str):
        """Calcula idade a partir de data DD/MM/AAAA.

        Args:
            data_str: Data de nascimento em string.

        Returns:
            str: Idade calculada ou N/A quando não for possível calcular.
        """
        if not data_str or data_str == "N/A":
            return "N/A"
        try:
            nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
            hoje = date.today()
            return str(hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day)))
        except Exception:
            return "N/A"

    # --- TABELA DE FUNCIONÁRIOS (Simplificada) ---
    print("\n" + "=" * 50)
    print(f"| {'BASE DE FUNCIONÁRIOS':^46} |")
    print("=" * 50)
    print(f"| {'NOME':^26} | {'CPF':^17} |")
    print("-" * 50)

    if not funcionarios:
        print(f"| {'Nenhum funcionário cadastrado.':^46} |")
    else:
        for f in funcionarios:
            nome = f.get("NOME", "Sem Nome")[:26]
            cpf = f.get("USUARIO", "Sem CPF")
            print(f"| {nome:<26} | {cpf:^17} |")
    print("-" * 50)

    # --- TABELA DE CLIENTES (Completa para Insights) ---
    print("\n" + "=" * 85)
    print(f"| {'BASE DE CLIENTES (DADOS PARA INSIGHTS)':^81} |")
    print("=" * 85)
    print(f"| {'NOME':^20} | {'CPF':^14} | {'IDADE':^7} | {'ENDEREÇO/CIDADE':^28} |")
    print("-" * 85)

    if not clientes:
        print(f"| {'Nenhum cliente cadastrado.':^81} |")
    else:
        for c in clientes:
            nome = c.get("NOME", "Sem Nome")[:20]
            cpf = c.get("USUARIO", "Sem CPF")
            idade = calcular_idade(c.get("NASCIMENTO", ""))
            endereco = c.get("ENDERECO", "N/A")[:28]

            print(f"| {nome:<20} | {cpf:^14} | {idade:^7} | {endereco:<28} |")
    print("-" * 85)


#==================================================================================================================
#==================================================================================================================


def fluxo_visualizar_base():
    """Abre submenu para consulta das bases CSV do sistema.

    Permite alternar entre visualização de quartos e de usuários.
    """
    while True:
        limpar_tela()
        print("\n" + "=" * 35)
        print(" " * 6 + "VISUALIZAR BASE DE DADOS")
        print("=" * 35 + "\n")

        print(" > [1] - Ver Base de Quartos")
        print(" > [2] - Ver Base de Usuários")
        print(" > [0] - Voltar")
        print("\n" + "-" * 35)

        opcao = input("\n >> Escolha o banco de dados: ").strip()

        if opcao == "1":
            limpar_tela()
            print_todos_os_quartos()  # Reutilizamos a tabela que já estava pronta!
            pausar_tela()

        elif opcao == "2":
            limpar_tela()
            print_todos_os_usuarios()
            pausar_tela()

        elif opcao == "0":
            break

        else:
            print(f"{VERMELHO}ERRO: Digite uma opção válida!{RESET}")
            pausar_tela()

#==================================================================================================================
#==================================================================================================================

def fluxo_fazer_reserva_funcionario():
    """Executa reserva em balcão para um cliente já cadastrado.

    O fluxo exige CPF válido no cadastro e segue as mesmas regras de
    disponibilidade do fluxo de reserva do cliente.
    """
    limpar_tela()
    print("\n" + "=" * 35)
    print(" "*6 + "NOVA RESERVA (BALCÃO)")
    print("=" * 35 + "\n")

    cpf_cliente = ler_cpf("  >> Digite o CPF do cliente (ou [0] para cancelar): ")
    if cpf_cliente == "0":
        return

    # Busca o nome do cliente no banco
    nome_cliente = buscar_nome_cliente_por_cpf(cpf_cliente)

    if not nome_cliente:
        print(f"\n{VERMELHO}ERRO: Cliente não encontrado no sistema!{RESET}")
        print(f"{AMARELO}Por favor, realize o cadastro do cliente primeiro (Opção 1 do menu).{RESET}")
        pausar_tela()
        return

    print(f"\n{VERDE}Cliente encontrado: {nome_cliente}{RESET}\n")

    if not tem_quarto_disponivel():
        print(f"\n{VERMELHO}Desculpe, o hotel está com 100% de ocupação no momento.{RESET}")
        pausar_tela()
        return

    print_quartos_disponiveis()
    quarto = ler_texto_obrigatorio("  >> Digite o número do quarto desejado: ").strip()

    if not quarto_esta_livre(quarto):
        print(f"\n{VERMELHO}ERRO: O quarto {quarto} não existe ou já está reservado!{RESET}")
        pausar_tela()
        return

    data_checkin = ler_data_futura("  >> Digite a data do Check-in (DD/MM/AAAA): ")
    dias = input("  >> Digite a quantidade de dias para a reserva: ").strip()

    # Passamos o nome que achamos no banco de dados
    mensagem_sucesso = fazer_checkin(nome_cliente, cpf_cliente, quarto, dias, data_checkin)

    print(f"\n{mensagem_sucesso}")
    pausar_tela()