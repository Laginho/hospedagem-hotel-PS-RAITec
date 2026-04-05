# 🏨 Hospedagem RAITec

Esse projeto foi desenvolvido pela Equipe 2 para o Desafio de Tecnologia. 

É um sistema de gerenciamento de hotel em CLI. Como banco de dados, usamos um arquivo `.csv` para a persistência das informações.

## Overview

Nós dividimos a aplicação em dois perfis de acesso principais:

### Portal do Cliente
- Criar uma conta e fazer login.
- Ver a lista de quartos disponíveis (com os preços).
- Fazer reservas (Check-in) escolhendo as datas.
- Consultar o histórico de reservas e o valor total da estadia.
- Cancelar reservas ativas.

### Portal do Funcionário
- Fazer reservas para clientes.
- Cadastrar novos clientes e novos funcionários.
- Finalizar a estadia, calcular o valor total (com regra de diária mínima) e liberar o quarto.
- Adicionar novos quartos, alterar valores de diária, colocar/tirar de manutenção e excluir quartos do sistema.
- Visualizar as bases de dados completas (clientes e quartos) formatadas em tabelas no próprio console.

## Tecnologias e Estrutura

O projeto foi feito em python puro, isto é, sem bibliotecas adicionais.

A arquitetura do projeto foi dividida em:
* `data/`: Nossos "bancos de dados" (arquivos CSV com as credenciais e estado dos quartos).
* `models/`: As classes base (POOs) do negócio (`Usuario`, `Cliente`, `Quarto`, etc).
* `services/`: A lógica pesada da aplicação (cálculos de datas, regras de negócio e leitura/escrita dos CSVs).
* `ui/`: Tudo relacionado ao que aparece na tela (menus, fluxos de interação).
* `utils/`: Validações de input do usuário (pra ninguém quebrar o sistema digitando letra onde é número) e configuração das cores do terminal.

## Como rodar

De pré-requisito, você precisa apenas ter o Python 3+ instalado.

1. Clone o repositório:
```bash
git clone [https://github.com/seu-usuario/hospedagem-hotel-PS-RAITec.git](https://github.com/seu-usuario/hospedagem-hotel-PS-RAITec.git)
```

2. Entre na pasta do projeto:
```bash
cd hospedagem-hotel-PS-RAITec
```

3. Execute o arquivo principal:
```bash
python main.py
```

## 🧑‍💻 Autores / Equipe 2

* Bruno Lage
* Francisco Davi Moreira
* Maria Eduarda de Lima Alves
