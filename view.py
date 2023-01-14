# --------------------------------------------------------------------------- #
# IMPORTAÇÕES


import sqlite3
import pandas as pd


# --------------------------------------------------------------------------- #
# CONEXÃO


connection = sqlite3.connect('data.db')


# --------------------------------------------------------------------------- #
# INSERÇÕES


def insert_category(category):
    """Função para insterir categoria em tabela"""
    with connection:
        cursor = connection.cursor()
        insertion = 'insert into Categoria (nome) values (?)'
        cursor.execute(insertion, category)


def insert_revenue(revenue):
    """Função para insterir receita em tabela"""
    with connection:
        cursor = connection.cursor()
        insertion = '''
            insert into Receitas(
                categoria,
                adicionado_em, valor
            )
            values (?, ?, ?)
        '''
        cursor.execute(insertion, revenue)


def insert_expenses(expenses):
    """Função para insterir gastos em tabela"""
    with connection:
        cursor = connection.cursor()
        insertion = '''
            insert into Gastos(
                categoria,
                retirado_em, valor
            )
            values (?, ?, ?)
        '''
        cursor.execute(insertion, expenses)


# --------------------------------------------------------------------------- #
# EDIÇÃO/ATUALIZAÇÃO


def update_instruction(record, category, amount):
    """Função que cuida da atualização dos dados da tabela."""

    # Monta a instrução de update, de acordo com os campos preenchidos.
    if record[1] == 'Receita':
        with connection:
            cursor = connection.cursor()
            update = 'update Receitas set valor = (?) where id = (?)'
            cursor.execute(update, [amount, record[0]])
    else:
        # Aqui, não tem perigo de fazer deste jeito, pois
        # no arquivo main já impeço de ter dois campos vazios
        # antes de chamar esta função.
        if category == '':
            new_category = record[1]
            new_amount = amount
        elif amount == '':
            new_category = category
            new_amount = record[3]
        else:
            new_category = category
            new_amount = amount

        with connection:
            cursor = connection.cursor()
            update_expense = '''
                update Gastos
                set categoria = (?),
                valor = (?)
                where id = (?)
                limit 1
            '''
            update_category = '''
                update Categoria
                set nome = (?)
                where id = (?)
            '''
            cursor.execute(
                update_expense,
                [new_category, new_amount, record[0]]
            )
            cursor.execute(update_category, [new_category, record[0]])


# --------------------------------------------------------------------------- #
# REMOÇÃO DAS TABELAS


def drop_tables():
    """Função que cuida de apagar a tabela toda."""
    with connection:
        cursor = connection.cursor()

        for item in ('Categoria', 'Receitas', 'Gastos'):
            cursor.execute(f'delete from {item}')


# --------------------------------------------------------------------------- #
# VISUALIZAÇÕES


def show_category_records():
    """Função para mostrar todos os registros da tabela categorias."""
    datalist = []
    with connection:
        cursor = connection.cursor()
        cursor.execute('select * from Categoria')
        records = cursor.fetchall()

        for record in records:
            datalist.append(record)

    return datalist


def show_revenue_records():
    """Função para mostrar todos os registros da tabela receitas."""
    datalist = []
    with connection:
        cursor = connection.cursor()
        cursor.execute('select * from Receitas')
        records = cursor.fetchall()

        for record in records:
            datalist.append(record)

    return datalist


def show_expenses_records():
    """Função para mostrar todos os registros da tabela gastos."""
    datalist = []
    with connection:
        cursor = connection.cursor()
        cursor.execute('select * from Gastos')
        records = cursor.fetchall()

        for record in records:
            datalist.append(record)

    return datalist


# --------------------------------------------------------------------------- #
# ATUALIZAÇÃO DOS GRÁFICOS, SUMÁRIO E TABELA


def table():
    """Função que cuida dos dados da tabela."""
    expenses = show_expenses_records()
    revenues = show_revenue_records()

    table_list = []

    for item in expenses:
        table_list.append(item)

    for item in revenues:
        table_list.append(item)

    return table_list


def bar_graph_values():
    """Função que cuida dos dados do gráfico de barra e do sumário."""

    # Receita total
    revenues = show_revenue_records()
    revenues_list = []

    for item in revenues:
        revenues_list.append(item[3])

    total_revenue = sum(revenues_list)

    # Despesas totais
    expenses = show_expenses_records()
    expenses_list = []

    for item in expenses:
        expenses_list.append(item[3])

    total_expenses = sum(expenses_list)

    # Saldo total
    total_credit = total_revenue - total_expenses
    return (total_revenue, total_expenses, total_credit)


def pie_graph_values():
    """Cuida dos dados do gráfico circular (pie)"""
    expenses = show_expenses_records()
    table_list = []

    for item in expenses:
        table_list.append(item)

    dataframe = pd.DataFrame(
        table_list,
        columns=[
            'id', 'categoria',
            'Data', 'valor'
        ]
    )

    dataframe = dataframe.groupby('categoria')['valor'].sum()

    amount_list = dataframe.values.tolist()
    category_list = []

    for item in dataframe.index:
        category_list.append(item)

    return ([category_list, amount_list])


def percentage_bar_values():
    """Cuida dos valores da barra de porcentagem."""

    # Aqui, se o não tiver dados, exemplo, se for a primeira vez
    # que executa o script ou se tiver deletado a tabela, dá erro por
    # causa da divisão por zero (ZeroDivision). Achei mais facil usar o if,
    # do que o try except (que ainda não me acostomei bem kk).
    if bar_graph_values()[1] == 0:
        return bar_graph_values()[0]
    else:
        return (
            (
                bar_graph_values()[0] - bar_graph_values()[1]
            ) / bar_graph_values()[0]) * 100
