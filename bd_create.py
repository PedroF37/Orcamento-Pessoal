import sqlite3


# Conexão
connection = sqlite3.connect('data.db')

'''
Segundo o que li na documentação do sqlite3, não é recomendado
usar o atributo autoincrement. Até porque pelo vi, o sqlite3
incrementa automaticamente o id (rowid), quando especificamos
id integer primary key.
'''

# tabela categoria
def create_category():
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''create table if not exists Categoria(
                    id integer primary key,
                    nome text
            )'''
        )

# tabela receita
def create_revenue():
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''create table if not exists Receitas(
                    id integer primary key,
                    categoria text,
                    adicionado_em date,
                    valor decimal
            )'''
        )

# tabela de gastos
def create_expenses():
    with connection:
        cursor = connection.cursor()
        cursor.execute(
            '''create table if not exists Gastos(
                    id integer primary key,
                    categoria text,
                    retirado_em date,
                    valor decimal
            )'''
        )
