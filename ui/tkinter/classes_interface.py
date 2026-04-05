from datetime import *
import tkinter as tk

from models.classes_raiteis import Cliente
from services.helper_db import autenticar_usuario_db, cadastrar_usuario_bd
from utils.validacoes import cpf_ja_cadastrado


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x600")
        self.frames = {}

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        for Tela in (MenuPrincipal, PortalCliente, PortalFuncionario,
             TelaLoginCliente, TelaCadastroCliente, MenuCliente):
            frame = Tela(self)
            self.frames[Tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar(MenuPrincipal)

    def mostrar(self, tela):
        self.frames[tela].tkraise()

class MenuPrincipal(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        titulo = tk.Label(self, text="SISTEMA DE HOSPEDAGEM RAITEIS", font=("Arial", 14))
        titulo.grid(row=0, column=0)
        boasvindas = tk.Label(self, text="Bem vindo!", font=("Arial", 11))
        boasvindas.grid(row=1, column=0)

        botoes=tk.Frame(self)
        botoes.grid(row=2, column=0)

        acessoCliente = tk.Button(botoes, text="Acesso Cliente", width=20,
                                  command=lambda: parent.mostrar(PortalCliente))
        acessoCliente.pack(pady=5)

        acessoFuncionario = tk.Button(botoes, text="Acesso Funcionário", width=20,
                                      command=lambda: parent.mostrar(PortalFuncionario))
        acessoFuncionario.pack(pady=5)

        sair = tk.Button(botoes, text = "Sair", width=20, command=lambda: exit())
        sair.pack(pady=5)

class PortalCliente(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="PORTAL DO CLIENTE", font=("Arial", 14)).grid(row=0, column=0, pady=10)

        botoes = tk.Frame(self)
        botoes.grid(row=2, column=0)

        tk.Button(botoes, text="Já sou cliente (Login)", width=20,
                  command=lambda: parent.mostrar(TelaLoginCliente)).pack(pady=5)
        tk.Button(botoes, text="Criar minha conta", width=20,
                  command=lambda: parent.mostrar(TelaCadastroCliente)).pack(pady=5)
        tk.Button(botoes, text="Voltar", width=20,
                  command=lambda: parent.mostrar(MenuPrincipal)).pack(pady=5)

class PortalFuncionario(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

class TelaLoginCliente(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="LOGIN DO CLIENTE", font=("Arial", 14)).grid(row=0, column=0, pady=10)

        form = tk.Frame(self)
        form.grid(row=1, column=0)

        tk.Label(form, text="CPF:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_cpf = tk.Entry(form, width=20)
        self.entry_cpf.grid(row=0, column=1)

        tk.Label(form, text="Senha:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_senha = tk.Entry(form, width=20, show="*")
        self.entry_senha.grid(row=1, column=1)

        self.msg_erro = tk.Label(self, text="", fg="red")
        self.msg_erro.grid(row=2, column=0)

        botoes = tk.Frame(self)
        botoes.grid(row=3, column=0, pady=10)

        tk.Button(botoes, text="Entrar", width=15,
                  command=lambda: self.tentar_login(parent)).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", width=15,
                  command=lambda: parent.mostrar(PortalCliente)).pack(side="left", padx=5)

    def tentar_login(self, parent):
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()

        conta = autenticar_usuario_db(cpf, senha, "Cliente")

        if conta:
            self.msg_erro.config(text="")
            cliente_logado = Cliente(nome=conta["NOME"], cpf=conta["USUARIO"], senha=conta["SENHA"])
            parent.frames[MenuCliente].definir_cliente(cliente_logado)
            parent.mostrar(MenuCliente)
        else:
            self.msg_erro.config(text="CPF ou senha incorretos.")

class TelaCadastroCliente(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(6, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="NOVO CADASTRO", font=("Arial", 14)).grid(row=0, column=0, pady=10)

        form = tk.Frame(self)
        form.grid(row=1, column=0)

        tk.Label(form, text="Nome:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_nome = tk.Entry(form, width=25)
        self.entry_nome.grid(row=0, column=1)

        tk.Label(form, text="CPF:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_cpf = tk.Entry(form, width=25)
        self.entry_cpf.grid(row=1, column=1)

        tk.Label(form, text="Senha:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_senha = tk.Entry(form, width=25, show="*")
        self.entry_senha.grid(row=2, column=1)

        tk.Label(form, text="Endereço:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_endereco = tk.Entry(form, width=25)
        self.entry_endereco.grid(row=3, column=1)

        tk.Label(form, text="Data de Nascimento (DD/MM/AAAA):").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_data = tk.Entry(form, width=25)
        self.entry_data.grid(row=4, column=1)

        self.msg = tk.Label(self, text="", fg="red")
        self.msg.grid(row=5, column=0)

        botoes = tk.Frame(self)
        botoes.grid(row=6, column=0, pady=10)

        tk.Button(botoes, text="Cadastrar", width=15,
                  command=lambda: self.tentar_cadastro(parent)).pack(side="left", padx=5)
        tk.Button(botoes, text="Voltar", width=15,
                  command=lambda: parent.mostrar(PortalCliente)).pack(side="left", padx=5)

    def tentar_cadastro(self, parent):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        senha = self.entry_senha.get().strip()
        endereco = self.entry_endereco.get().strip()
        data = self.entry_data.get().strip()

        if not nome or not cpf or not senha:
            self.msg.config(text="Preencha todos os campos.", fg="red")
            return

        if not cpf.isdigit():
            self.msg.config(text="CPF deve conter apenas números.", fg="red")
            return

        if cpf_ja_cadastrado(cpf):
            self.msg.config(text="Este CPF já possui cadastro.", fg="red")
            return

        if data:
            try:
                datetime.strptime(data, "%d/%m/%Y")
            except ValueError:
                self.msg.config(text="Data inválida. Use o formato DD/MM/AAAA.", fg="red")
                return

        cadastrar_usuario_bd("Cliente", nome, cpf, senha, data, endereco)
        self.msg.config(text="Conta criada com sucesso!", fg="green")

        # Limpa os campos após o cadastro
        self.entry_nome.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)
        self.entry_senha.delete(0, tk.END)
        self.entry_endereco.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)

class MenuCliente(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.cliente_atual = None

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="ÁREA DO CLIENTE", font=("Arial", 14)).grid(row=0, column=0, pady=10)

        self.label_boas_vindas = tk.Label(self, text="", font=("Arial", 10))
        self.label_boas_vindas.grid(row=1, column=0)

        botoes = tk.Frame(self)
        botoes.grid(row=2, column=0, pady=10)

        tk.Button(botoes, text="Ver quartos disponíveis", width=25,
                  command=self.ver_quartos).pack(pady=5)
        tk.Button(botoes, text="Fazer reserva", width=25,
                  command=self.fazer_reserva).pack(pady=5)
        tk.Button(botoes, text="Consultar minhas reservas", width=25,
                  command=self.consultar_reservas).pack(pady=5)
        tk.Button(botoes, text="Cancelar minha reserva", width=25,
                  command=self.cancelar_reserva).pack(pady=5)
        tk.Button(botoes, text="Sair", width=25,
                  command=lambda: parent.mostrar(MenuPrincipal)).pack(pady=5)

    def definir_cliente(self, cliente):
        self.cliente_atual = cliente
        self.label_boas_vindas.config(text=f"Bem-vindo(a), {cliente.nome}!")

    def ver_quartos(self):
        pass

    def fazer_reserva(self):
        pass

    def consultar_reservas(self):
        pass

    def cancelar_reserva(self):
        pass