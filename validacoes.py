from datetime import datetime

def ler_texto_obrigatorio(mensagem):
    #Garante que o usuário não deixe o campo em branco.
    while True:
        texto = input(mensagem).strip()
        if texto == "":
            print("ERRO: Esse campo é obrigatório e não pode ficar vazio.")
        else:
            return texto


def ler_numero_inteiro(mensagem):
    #Garante que o usuário digite um número inteiro válido.
    while True:
        valor = input(mensagem).strip()
        if valor == "":
            print("ERRO: Esse campo não pode ficar vazio.")
            continue

        try:
            # Tenta converter o texto para inteiro
            numero = int(valor)
            return numero
        except ValueError:
            # Se quebrar (ex: digitou letra), avisa o erro
            print("ERRO: Digite apenas números inteiros. Letras não são aceitas.")


def ler_data(mensagem):
    #Garante que o usuário digite uma data real no formato DD/MM/AAAA.
    while True:
        data_str = input(mensagem).strip()
        if data_str == "":
            print("ERRO: A data é obrigatória.")
            continue

        try:
            #O strptime tenta encaixar a string no formato de data
            data_valida = datetime.strptime(data_str, "%d/%m/%Y")

            #Se passar retorna a data bonitinha como string
            return data_valida.strftime("%d/%m/%Y")
        except ValueError:
            print("ERRO: Data inválida ou formato incorreto. Use DD/MM/AAAA")