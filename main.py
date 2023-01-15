# --------------------------------------------------------------------------- #
# IMPORTAÇÕES


# tkinter
from tkinter import Tk, Frame, Label, Button, Entry, messagebox
from tkinter.ttk import Style, Progressbar, Treeview, Scrollbar, Combobox

# Pillow
from PIL import Image, ImageTk

# tkcalendar
from tkcalendar import DateEntry

# matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# view
from view import insert_category, insert_revenue, insert_expenses
from view import show_category_records, drop_tables
from view import table, bar_graph_values, update_instruction
from view import pie_graph_values, percentage_bar_values

# bd_create
from bd_create import create_category, create_revenue, create_expenses

# re
import re


# --------------------------------------------------------------------------- #
# CONSTANTES E GLOBAIS


COLOR0 = "#2e2d2b"
COLOR1 = "#feffff"
COLOR2 = "#4fa882"
COLOR3 = "#38576b"
COLOR4 = "#403d3d"
COLOR5 = "#e06636"
COLOR6 = "#038cfc"
COLOR7 = "#3fbfb9"
COLOR8 = "#263238"
COLOR9 = "#e9edf5"
COLOR10 = '#545454'
COLOR11 = '#83a9e6'

COLORS = [
    '#5588bb', '#66bbbb',
    '#99bb55', '#ee9944',
    '#444466', '#bb5555'
]


# Padrões para validações das Entries
string_pattern = r'^[A-Za-z]+( [A-Za-z]+)*$'
number_pattern = r'^\d+$'


global tree


# --------------------------------------------------------------------------- #
# FUNÇÕES


def manipulate_tables():
    """Função que cuida de deletar e criar as tabelas."""
    drop_tables()
    refresh_data()
    messagebox.showinfo(
        'Sucesso', f'Dados deletados com sucesso. A visualização' \
        f' pode ficar estranha enquanto não reiniciar o aplicativo.'
    )


def percentage():
    """Função para mostrar a percentagem."""
    percent_message_label = Label(
        middle_frame, text='Porcentagem da receita restante',
        height=1, anchor='nw', font=('Verdana 12'),
        bg=COLOR1, fg=COLOR4
    )
    percent_message_label.place(x=7, y=5)

    style = Style()
    style.theme_use('default')
    style.configure(
        'black.Horizontal.TProgressbar',
        background='#daed6b'
    )
    style.configure('TProgressbar', thickness=25)

    progressbar = Progressbar(
        middle_frame, length=180,
        style='black.Horizontal.TProgressbar'
    )
    progressbar.place(x=10, y=35)
    progressbar['value'] = percentage_bar_values()

    percent_value = percentage_bar_values()
    percent_number_label = Label(
        middle_frame, text=f'{percent_value:,.2f}%',
        anchor='nw', font=('Verdana 12'),
        bg=COLOR1, fg=COLOR4
    )
    percent_number_label.place(x=200, y=35)


def bar_graph():
    """Função que cuida do gráfico de barra."""
    category_list = ['Renda', 'Despesas', 'Saldo']
    values_list = bar_graph_values()

    # O gráfico e os eixos. Esta parte dos gráficos
    # foi muito copy/paste. matplotlib ainda é meio
    # "chinês" para mim kk.
    graph = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = graph.add_subplot(111)
    # ax.autoscale(enable=True, axis='both', tight=None)

    ax.bar(category_list, values_list, color=COLORS, width=0.9)

    c = 0
    for item in ax.patches:
        ax.text(
            item.get_x() - .001, item.get_height() + .5,
            f'{values_list[c]:,.0f}', fontsize=17,
            fontstyle='italic', verticalalignment='bottom',
            color='dimgrey'
        )

        c += 1

    ax.set_xticklabels(category_list, fontsize=16)

    # Personalizando o gráfico
    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)

    canvas = FigureCanvasTkAgg(graph, middle_frame)
    canvas.get_tk_widget().place(x=10, y=70)


def summary():
    """Função que cuida do sumário da renda e despesas."""
    values = bar_graph_values()

    # Renda Mensal
    line_label = Label(
        middle_frame, text='',
        width=215, height=1,
        anchor='nw', font=('Arial 1'),
        bg=COLOR10
    )
    # line_label.place(x=349, y=52)
    line_label.place(x=500, y=52)

    summary_label = Label(
        middle_frame, text='TOTAL RENDA MENSAL      ',
        anchor='nw', font=('Verdana 12'),
        bg=COLOR1, fg=COLOR11
    )
    # summary_label.place(x=349, y=33)
    summary_label.place(x=500, y=33)

    value_label = Label(
        middle_frame, text=f'R$ {values[0]:,.2f}',
        anchor='nw', font=('Arial 17'),
        bg=COLOR1, fg=COLOR10
    )
    # value_label.place(x=349, y=70)
    value_label.place(x=500, y=70)

    # Despesas Mensais
    line_label = Label(
        middle_frame, text='',
        width=215, height=1,
        anchor='nw', font=('Arial 1'),
        bg=COLOR10
    )
    # line_label.place(x=349, y=132)
    line_label.place(x=500, y=132)

    summary_label = Label(
        middle_frame, text='TOTAL DESPESAS MENSAIS',
        anchor='nw', font=('Verdana 12'),
        bg=COLOR1, fg=COLOR11
    )
    # summary_label.place(x=349, y=113)
    summary_label.place(x=500, y=113)

    value_label = Label(
        middle_frame, text=f'R$ {values[1]:,.2f}',
        anchor='nw', font=('Arial 17'),
        bg=COLOR1, fg=COLOR10
    )
    # value_label.place(x=349, y=150)
    value_label.place(x=500, y=150)

    # Saldo Total
    line_label = Label(
        middle_frame, text='',
        width=215, height=1,
        anchor='nw', font=('Arial 1'),
        bg=COLOR10
    )
    # line_label.place(x=349, y=212)
    line_label.place(x=500, y=212)

    summary_label = Label(
        middle_frame, text='SALDO TOTAL DA CAIXA   ',
        anchor='nw', font=('Verdana 12'),
        bg=COLOR1, fg=COLOR11
    )
    # summary_label.place(x=349, y=193)
    summary_label.place(x=500, y=193)

    value_label = Label(
        middle_frame, text=f'R$ {values[2]:,.2f}',
        anchor='nw', font=('Arial 17'),
        bg=COLOR1, fg=COLOR10
    )
    # value_label.place(x=349, y=230)
    value_label.place(x=500, y=230)


def pie_graph():
    """Função que cuida do gráfico circular (pie graph)."""
    graph = plt.Figure(figsize=(5, 3), dpi=90)
    ax = graph.add_subplot(111)

    category_list = pie_graph_values()[0]   # Categoria
    values_list = pie_graph_values()[1]     # Valores

    explode = []
    for item in category_list:
        explode.append(0.05)

    ax.pie(
        values_list, explode=explode,
        wedgeprops=dict(width=0.2),
        autopct='%1.1f%%', colors=COLORS,
        shadow=True, startangle=90
    )
    ax.legend(
        category_list,
        loc="center right",
        bbox_to_anchor=(1.55, 0.50)
    )

    category_canvas = FigureCanvasTkAgg(graph, pie_graph_frame)
    category_canvas.get_tk_widget().place(x=130, y=10)


def show_table():
    """Função que cuida de mostrar a tabela dos dados."""
    global tree
    table_label = Label(
        middle_frame, text='Tabela Receitas e Despesas',
        anchor='nw', font=('Verdana 12'), bg=COLOR1, fg=COLOR4
    )
    table_label.place(x=5, y=309)

    table_header = ['#id', 'Categoria', 'Data', 'Quantia']
    records = table()

    tree = Treeview(
        table_frame, selectmode='extended',
        columns=table_header, show='headings'
    )

    # Barra de rolagem vertical
    vsb = Scrollbar(table_frame, orient='vertical', command=tree.yview)

    # Barra de rolagem horizontal
    hsb = Scrollbar(table_frame, orient='horizontal', command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    # Posicionamento
    hd = ['center', 'center', 'center', 'center']
    h = [30, 100, 100, 100]
    n = 0

    for item in table_header:
        tree.heading(item, text=item.title(), anchor='center')
        tree.column(item, width=h[n], anchor=hd[n])

        n += 1

    for item in records:
        tree.insert('', 'end', values=item)


def insert_new_category():
    """Função que cuida da inserção de novas categorias."""
    category_name = [new_category_entry.get()]

    # Validação
    for item in category_name:
        if item == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Só aceita alfabeto
    category_string = ' '.join(category_name)
    if re.fullmatch(string_pattern, category_string) is None:
        messagebox.showerror('Erro', 'Categoria aceita apenas letras')
        return
    else:
        insert_category(category_name)
        messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
        reset_widgets(new_category_entry)

    # Pegando os valores da categoria
    categories = show_category_records()
    category = []

    for item in categories:
        # item[1] -> categoria/ item[0] -> id
        category.append(item[1])

    # atualizando dados
    expense_category_combo['values'] = (category)


def insert_new_renevue():
    """Função que cuida da inserção de novas receitas."""
    revenue_name = 'Receita'
    revenue_date = revenue_calendar_entry.get()
    revenue_value = total_value_revenue_entry.get()

    insert_revenue_list = [revenue_name, revenue_date, revenue_value]

    # Validação
    for item in insert_revenue_list:
        if item == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return

    # Só aceita numérico em revenue_value
    if re.fullmatch(number_pattern, revenue_value) is None:
        messagebox.showerror(
            'Erro', 'Quantia aceita apenas digitos [0-9]'
        )
        return
    else:
        insert_revenue(insert_revenue_list)
        messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')
        reset_widgets(revenue_calendar_entry, total_value_revenue_entry)

    # atualizando dados
    refresh_data()


def insert_new_expenses():
    """Função que cuida da inserção de novas despesas."""

    # Não pode inserir nada se ainda não tiver receita nunhuma.
    # bar_graph_values()[0] == valor total da receita.
    if bar_graph_values()[0] == 0:
        messagebox.showerror(
            'Erro',
            'Não pode inserir despesas sem ter uma receita antes'
        )
        return
    else:
        expense_name = expense_category_combo.get()
        expense_date = expense_calendar_entry.get()
        expense_value = total_value_expense_entry.get()

        insert_expense_list = [expense_name, expense_date, expense_value]

        # Validação
        for item in insert_expense_list:
            if item == '':
                messagebox.showerror('Erro', 'Preencha todos os campos')
                return

        # Só aceita numérico em expense_value
        if re.fullmatch(number_pattern, expense_value) is None:
            messagebox.showerror(
                'Erro', 'Quantia aceita apenas digitos [0-9]'
            )
            return
        else:
            insert_expenses(insert_expense_list)
            messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso')

    reset_widgets(
        expense_category_combo,
        expense_calendar_entry,
        total_value_expense_entry
    )
    # atualizando dados
    refresh_data()


def reset_widgets(*widgets):
    """Função que reseta os entries e combos depois de inserções."""
    for widget in widgets:
        widget.delete(0, 'end')
    return


def refresh_data():
    """Função que cuida de atualizar
    os dados depois de inserções/remoções."""
    percentage()
    summary()
    bar_graph()
    pie_graph()
    show_table()
    return


def edit_data():
    """Função que cuida de editar/alterar dados da tabela."""
    replaced_category = alter_category_entry.get()
    replaced_amount = alter_value_entry.get()

    if tree.focus() == '':
        messagebox.showerror(
            'Erro',
            'Tem que selecionar um registro na TABELA da esquerda para alterar'
        )
        return
    else:
        treeview_data = tree.focus()
        treeview_dict = tree.item(treeview_data)
        treeview_list = treeview_dict['values']

        # Aqui, obrigo a preencher apenas um dos campos e não os dois,
        # porque podemos querer mudar apenas o valor do aluguél por exemplo,
        # ou pudemos queres mudar apenas o nome da despesa. Ou os dois kk
        if replaced_category == '' and replaced_amount == '':
            messagebox.showerror(
                'Erro', 'Tem que preencher pelo menos um dos campos'
            )
            return
        else:
            # Agora temos que validar o ou os inputs
            if replaced_category != '':
                # Só alfabeto
                if re.fullmatch(string_pattern, replaced_category) is None:
                    messagebox.showerror(
                        'Erro', 'Categoria aceita apenas letras'
                    )
                    return

            if replaced_amount != '':
                # Só digito
                if re.fullmatch(number_pattern, replaced_amount) is None:
                    messagebox.showerror(
                        'Erro', 'Quantia aceita apenas digitos [0-9]'
                    )
                    return

        update_instruction(
            treeview_list, replaced_category, replaced_amount
        )
        messagebox.showinfo('Sucesso', 'Dados atualizados com sucesso')
        refresh_data()
        reset_widgets(alter_category_entry, alter_value_entry)


# --------------------------------------------------------------------------- #
# CRIA TABELAS CASO NECESSÁRIO


# Instrução sql em bd_create é: create if not exists
# logo se já existir não faz nada ok?!
create_category()
create_revenue()
create_expenses()


# --------------------------------------------------------------------------- #
# JANELA


window = Tk()
window.title('')
window.geometry('1320x648')
window.resizable(width=False, height=False)
# window.configure(background=COLOR9)

style = Style(window)
style.theme_use('clam')


# --------------------------------------------------------------------------- #
# FRAMES, TÍTULO E LOGO


# Frames principais
upper_frame = Frame(
    window, width=1320,
    height=50, bg=COLOR1,
    relief='flat'
)
upper_frame.grid(row=0, column=0, padx=0)

middle_frame = Frame(
    window, width=1320, height=361,
    bg=COLOR1, pady=20, relief='raised'
)
middle_frame.grid(
    row=1, column=0,
    pady=1, padx=0,
    sticky='nsew'
)

lower_frame = Frame(
    window, width=1320, height=237,
    bg=COLOR1, relief='flat'
)
lower_frame.grid(
    row=2, column=0,
    pady=0, padx=0,
    sticky='nsew'
)


# Frames dentro de Frames
pie_graph_frame = Frame(
    middle_frame, width=580,
    height=250, bg=COLOR1
)
# pie_graph_frame.place(x=415, y=5)
pie_graph_frame.place(x=720, y=5)

table_frame = Frame(
    lower_frame, width=330,
    height=237, bg=COLOR1
)
table_frame.grid(row=0, column=0)

expenses_insert_frame = Frame(
    lower_frame, width=330,
    height=237, bg=COLOR1
)
expenses_insert_frame.grid(row=0, column=1, padx=5)

revenue_insert_frame = Frame(
    lower_frame, width=330,
    height=237, bg=COLOR1
)
revenue_insert_frame.grid(row=0, column=2)

alter_table_frame = Frame(
    lower_frame, width=330,
    height=237, bg=COLOR1
)
alter_table_frame.grid(row=0, column=3)


# Título e logo do app
img = Image.open('Icones/money-bag.png')
img = img.resize((45, 45))
img = ImageTk.PhotoImage(img)

title_label = Label(
    upper_frame, image=img,
    text=' Controle de Receitas e Despesas',
    width=1400, compound='left',
    padx=5, relief='raised',
    anchor='nw', bg=COLOR1,
    fg=COLOR4, font=('Verdana 20 bold')
)
title_label.grid(row=0, column=0)


# --------------------------------------------------------------------------- #
# DESPESAS


expenses_label = Label(
    expenses_insert_frame,
    text='Insira novas Despesas',
    height=1, anchor='nw',
    font=('Verdana 10 bold'),
    bg=COLOR1, fg=COLOR4
)
expenses_label.place(x=10, y=5)

# Categoria das despesas
category_label = Label(
    expenses_insert_frame,
    text='Categoria',
    height=1, anchor='nw',
    font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
category_label.place(x=10, y=40)

# Pegandos categorias
categories_list = show_category_records()
categories = []

for category in categories_list:
    categories.append(category[1])

expense_category_combo = Combobox(
    expenses_insert_frame,
    width=10, font=('Roboto 10')
)
expense_category_combo['values'] = (categories)
expense_category_combo.place(x=110, y=41)

# Data das despesas
expense_date_label = Label(
    expenses_insert_frame,
    text='Data', height=1,
    anchor='nw', font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
expense_date_label.place(x=10, y=70)

expense_calendar_entry = DateEntry(
    expenses_insert_frame,
    width=9, background='darkgrey',
    foreground='white', year=2023,
    borderwidth=2
)
expense_calendar_entry.place(x=110, y=71)

# Quantia total das despesas
total_value_expense_label = Label(
    expenses_insert_frame,
    text='Quantia Total',
    height=1, anchor='nw',
    font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
total_value_expense_label.place(x=10, y=102)

total_value_expense_entry = Entry(
    expenses_insert_frame,
    width=10, justify='left',
    relief='solid'
)
total_value_expense_entry.place(x=110, y=101)

# Botão adicionar
add_expenses_img = Image.open('Icones/add.png')
add_expenses_img = add_expenses_img.resize((17, 17))
add_expenses_img = ImageTk.PhotoImage(add_expenses_img)

insert_expenses_button = Button(
    expenses_insert_frame,
    image=add_expenses_img,
    text='ADICIONAR', width=68,
    compound='left', anchor='se',
    font=('Roboto 7 bold'), bg=COLOR1,
    fg=COLOR4, overrelief='ridge',
    command=insert_new_expenses
)
insert_expenses_button.place(x=110, y=141)


# --------------------------------------------------------------------------- #
# RECEITAS


revenues_label = Label(
    revenue_insert_frame,
    text='Insira novas Receitas/Categorias',
    height=1, anchor='nw', font=('Verdana 10 bold'),
    bg=COLOR1, fg=COLOR4
)
revenues_label.place(x=10, y=5)

# Data das receitas
revenue_date_label = Label(
    revenue_insert_frame, text='Data',
    height=1, anchor='nw', font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
revenue_date_label.place(x=10, y=40)

revenue_calendar_entry = DateEntry(
    revenue_insert_frame, width=9,
    background='darkgrey', foreground='white',
    borderwidth=2, year=2023
)
revenue_calendar_entry.place(x=110, y=41)

# Quantia total das receitas
total_value_revenue_label = Label(
    revenue_insert_frame, text='Quantia Total',
    height=1, anchor='nw', font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
total_value_revenue_label.place(x=10, y=74)

total_value_revenue_entry = Entry(
    revenue_insert_frame, width=10,
    justify='left', relief='solid'
)
total_value_revenue_entry.place(x=110, y=71)

add_revenue_img = Image.open('Icones/add.png')
add_revenue_img = add_revenue_img.resize((17, 17))
add_revenue_img = ImageTk.PhotoImage(add_revenue_img)

insert_revenue_button = Button(
    revenue_insert_frame,
    image=add_revenue_img,
    text='ADICIONAR', width=68,
    compound='left', anchor='se',
    font=('Roboto 7 bold'),
    bg=COLOR1, fg=COLOR4,
    overrelief='ridge',
    command=insert_new_renevue
)
insert_revenue_button.place(x=110, y=111)


# --------------------------------------------------------------------------- #
# NOVA CATEGRIA


new_category_label = Label(
    revenue_insert_frame,
    text='Nova Categoria',
    height=1, anchor='nw',
    font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
new_category_label.place(x=10, y=163)

new_category_entry = Entry(
    revenue_insert_frame, width=10,
    justify='left', relief='solid'
)
new_category_entry.place(x=110, y=161)

add_category_img = Image.open('Icones/add.png')
add_category_img = add_category_img.resize((17, 17))
add_category_img = ImageTk.PhotoImage(add_category_img)

insert_new_category_button = Button(
    revenue_insert_frame,
    image=add_category_img,
    text='ADICIONAR', width=68,
    compound='left', anchor='se',
    font=('Roboto 7 bold'),
    bg=COLOR1, fg=COLOR4,
    overrelief='ridge',
    command=insert_new_category
)
insert_new_category_button.place(x=110, y=195)


# --------------------------------------------------------------------------- #
# ALTERAR DADOS DA TABELA


alter_data_label = Label(
    alter_table_frame,
    text='Alterar/Deletar Tabela',
    height=1, anchor='nw',
    font=('Verdana 10 bold'),
    bg=COLOR1, fg=COLOR4
)
alter_data_label.place(x=70, y=5)

# Categoria das despesas
alter_category_label = Label(
    alter_table_frame,
    text='Categoria',
    height=1, anchor='nw',
    font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
alter_category_label.place(x=70, y=40)

alter_category_entry = Entry(
    alter_table_frame, width=10,
    justify='left', relief='solid'
)
alter_category_entry.place(x=170, y=41)

alter_value_label = Label(
    alter_table_frame, text='Quantia Total',
    height=1, anchor='nw', font=('Roboto 10'),
    bg=COLOR1, fg=COLOR4
)
alter_value_label.place(x=70, y=108)

alter_value_entry = Entry(
    alter_table_frame, width=10,
    justify='left', relief='solid'
)
alter_value_entry.place(x=170, y=101)

alter_img = Image.open('Icones/replace.png')
alter_img = alter_img.resize((17, 17))
alter_img = ImageTk.PhotoImage(alter_img)

alter_button = Button(
    alter_table_frame,
    image=alter_img,
    text='ALTERAR     ', width=68,
    compound='left', anchor='se',
    font=('Roboto 7 bold'),
    bg=COLOR1, fg=COLOR4,
    overrelief='ridge',
    command=edit_data
)
alter_button.place(x=170, y=131)


# --------------------------------------------------------------------------- #
# DELETAR TODA A TABELA


destroy_label = Label(
    alter_table_frame,
    text='Apagar tabela',
    height=1, anchor='nw',
    font=('Roboto 10 bold'),
    bg=COLOR1, fg=COLOR4
)
destroy_label.place(x=70, y=197)

destroy_img = Image.open('Icones/delete.png')
destroy_img = destroy_img.resize((17, 17))
destroy_img = ImageTk.PhotoImage(destroy_img)

# Os espaços são propositais. Para os icones
# adicionar e deletar ficarem alinhados.
destroy_button = Button(
    alter_table_frame,
    image=destroy_img,
    text='DELETAR     ',
    width=68, compound='left',
    anchor='se', font=('Roboto 7 bold'),
    bg=COLOR1, fg=COLOR4, overrelief='ridge',
    command=manipulate_tables
)
destroy_button.place(x=170, y=191)


# --------------------------------------------------------------------------- #
# LOOP


percentage()
summary()
bar_graph()
pie_graph()
show_table()
window.mainloop()
