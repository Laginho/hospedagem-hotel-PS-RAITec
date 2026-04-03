from datetime import date, timedelta
from helper_db import save_csv, parse_csv

class Funcionario:
    def __init__(self, nome, cpf, senha):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha
        #TODO LOGIN?
    def validar_login(self, senha):
        if senha == self.senha:
            return True
        else:
            return False

#classe dos clientes (hóspedes)
class Cliente:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf  #identificador único
        self.reservas = []

    def getNome(self): return self.nome
    def getCPF(self): return self.cpf
    def getReservas(self): return self.reservas
    def addReserva(self, reserva):
        self.reservas.append(reserva)
    #TODO? Printar as reservas?

    def validar_login(self, senha):
        contas = parse_csv("credenciais.csv")
        for conta in contas:
            if conta["TIPO"] == "Cliente" and conta["USUARIO"] == self.cpf and conta["SENHA"] == senha:
                return True
        return False

#classe das reservas
class Reserva:
    def __init__(self, cliente, quarto, data_inicio, dias):
        self.cliente = cliente
        self.quarto = quarto
        self.quarto.flipOcupado()
        # convertendo a data se ela vier em string
        if isinstance(data_inicio, str):
            data_inicio = date.fromisoformat(data_inicio)
        self.checkin = data_inicio
        # soma dos dias pra checkout
        self.checkout = data_inicio + timedelta(days=dias)

    def getCliente(self): return self.cliente
    def getQuarto(self): return self.quarto
    def getCheckin(self): return self.checkin
    def getCheckout(self): return self.checkout
    #TODO Resolver isso de a reserva tem um cliente e um quarto pois nao me decidi

#classe dos quartos
class Quarto:
    def __init__(self, numero):
        self.numero = str(numero)
        self.ocupado = False

    def getNumero(self): return self.numero
    def getOcupado(self): return self.ocupado
    # ocupar/desocupar um quarto
    def flipOcupado(self): self.ocupado = not self.ocupado


#cpf é em int ou em string????? duvida cruel

# teste
# c1 = Cliente("tom", 1234)
# c2 = Cliente("jerry", 12345)
# print(c1.getNome()+" "+str(c1.getCPF())+" ")
# print(c2.getNome()+" "+str(c2.getCPF())+" ")
# q1 = Quarto("101")
# q2 = Quarto("102")
# q3 = Quarto("103")
# r1 = Reserva(c1, q1, date.today(), 5)
# print(str(r1.getQuarto().getNumero())+" "+str(r1.getQuarto().getOcupado())+" "+str(r1.getCheckin())+" "+str(r1.getCheckout()))
#f1 = Funcionario("Fernando", 1234, "1234")
#print(f1.validar_login("12345"))
#print(f1.validar_login("1234"))