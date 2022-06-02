from tkinter import *
from tkinter import ttk, messagebox
import customtkinter
import sqlite3

from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter, A4
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

customtkinter.set_appearance_mode("system")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

janela = customtkinter.CTk()


class validadores:

    def validate_entry3(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 100

    def validate_entry2(self, text):
        if text == "": return True
        try:
            value = int(text)
        except ValueError:
            return False
        return 0 <= value <= 99999999999


class Relatorios:
    def __init__(self):
        self.telefonerel = None
        self.codigorel = None
        self.nomerel = None
        self.cidaderel = None
        self.c = None
        self.entry_telefone = None
        self.entry_cidade = None
        self.entry_nome = None
        self.entry_codigo = None

    def printcliente(self):
        webbrowser.open("cliente.pdf")

    def gerarelatorio(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigorel = self.entry_codigo.get()
        self.nomerel = self.entry_nome.get()
        self.telefonerel = self.entry_telefone.get()
        self.cidaderel = self.entry_cidade.get()

        self.c.setFont("Helvetica-Bold", 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont("Helvetica-Bold", 18)
        self.c.drawString(50, 700, 'Codigo: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 630, 'Telefone: ')
        self.c.drawString(50, 600, 'Cidade: ')

        self.c.setFont("Helvetica", 18)
        self.c.drawString(150, 700, self.codigorel)
        self.c.drawString(150, 670, self.nomerel)
        self.c.drawString(150, 630, self.telefonerel)
        self.c.drawString(150, 600, self.cidaderel)

        self.c.rect(20, 550, 550, 4, fill=False, stroke=True)

        self.c.showPage()
        self.c.save()
        self.printcliente()


class Func:
    def __init__(self):
        self.cidade = None
        self.codigo = None
        self.conec = None
        self.cursor = None
        self.telefone = None
        self.nome = None
        self.listaclientes = None
        self.entry_cidade = None
        self.entry_telefone = None
        self.entry_nome = None
        self.entry_codigo = None

    def limpa_tela(self):
        self.entry_codigo.delete(0, END)
        self.entry_nome.delete(0, END)
        self.entry_telefone.delete(0, END)
        self.entry_cidade.delete(0, END)

    def conecta_bd(self):
        self.conec = sqlite3.connect("cliente.db")
        self.cursor = self.conec.cursor()
        print("Conectando ao Banco de Dados")

    def desconecta_bd(self):
        self.conec.close()
        print("Desconectando o Banco de Dados")

    def montatabelas(self):
        self.conecta_bd()
        # Criar Tabela
        self.cursor.execute("""
            CREATE TABLE  IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );             
        """)
        self.conec.commit()
        print("Banco de Dados Criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.entry_codigo.get()
        self.nome = self.entry_nome.get()
        self.telefone = self.entry_telefone.get()
        self.cidade = self.entry_cidade.get()

    def add_cliente(self):
        self.variaveis()
        if self.entry_nome.get() == "":
            msg = "Para cadastrar um novo cliente é necessário \n"
            msg += "que seja digitado pelo menos um nome"
            messagebox.showinfo("Cadastro de clientes - AVISO!!!", msg)
        else:
            self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
            VALUES (?, ?, ?)""", (self.nome, self.telefone, self.cidade))
        self.conec.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.listaclientes.delete(*self.listaclientes.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.listaclientes.insert("", END, values=i)
        self.desconecta_bd()

    def duploclick(self, event):
        self.limpa_tela()
        self.listaclientes.selection()

        for n in self.listaclientes.selection():
            col1, col2, col3, col4 = self.listaclientes.item(n, 'values')
            self.entry_codigo.insert(END, col1)
            self.entry_nome.insert(END, col2)
            self.entry_telefone.insert(END, col3)
            self.entry_cidade.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM clientes WHERE cod = ? """, (self.codigo,))
        self.conec.commit()
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
        WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conec.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaclientes.delete(*self.listaclientes.get_children())

        self.entry_nome.insert(END, '%')
        nome = self.entry_nome.get()
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscarnomecli = self.cursor.fetchall()
        for i in buscarnomecli:
            self.listaclientes.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()


class Aplication(Func, Relatorios, validadores):
    def __init__(self):
        super().__init__()
        self.lb_nome = None
        self.lb_codigo = None
        self.frame_1 = None
        self.bt_apagar = None
        self.lb_telefone = None
        self.lb_cidade = None
        self.scroll_lista = None
        self.frame_2 = None
        self.bt_novo = None
        self.bt_alterar = None
        self.bt_buscar = None
        self.bt_limpar = None
        self.janela = janela
        self.valida_entradas1()
        self.valida_entradas2()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montatabelas()
        self.select_lista()
        self.menus()
        janela.mainloop()

    def tela(self):
        self.janela.title("Cadastro de Clientes")
        # self.janela.configure(background='#1e3743')
        self.janela.geometry("700x500")
        self.janela.resizable(True, True)
        self.janela.maxsize(width=900, height=700)
        self.janela.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.janela, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.janela, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # Botão de Limpar
        self.bt_limpar = customtkinter.CTkButton(master=self.frame_1, text="Limpar", command=self.limpa_tela,
                                                 text_color='WHITE', width=50, height=32,
                                                 text_font=('verdana', 8, 'bold'), border_width=0, corner_radius=8)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão de Buscar
        self.bt_buscar = customtkinter.CTkButton(master=self.frame_1, text="Buscar", command=self.busca_cliente,
                                                 text_color='WHITE', width=50, height=32,
                                                 text_font=('verdana', 8, 'bold'), border_width=0, corner_radius=8)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão de Novo
        self.bt_novo = customtkinter.CTkButton(master=self.frame_1, text="Novo", command=self.add_cliente,
                                               text_color='WHITE', width=50, height=32,
                                               text_font=('verdana', 8, 'bold'), border_width=0, corner_radius=8)
        self.bt_novo.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão de Alterar
        self.bt_alterar = customtkinter.CTkButton(master=self.frame_1, text="Alterar", command=self.altera_cliente,
                                                  text_color='WHITE', width=50, height=32,
                                                  text_font=('verdana', 8, 'bold'), border_width=0, corner_radius=8)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        # Botão de Apagar
        self.bt_apagar = customtkinter.CTkButton(master=self.frame_1, text="Apagar", command=self.deleta_cliente,
                                                 text_color='WHITE', width=50, height=32,
                                                 text_font=('verdana', 8, 'bold'), border_width=0, corner_radius=8)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        # Criação de Label e entrada de CÓDIGO
        self.lb_codigo = Label(self.frame_1, text='Código', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_codigo.place(relx=0.05, rely=0.05)

        self.entry_codigo = customtkinter.CTkEntry(master=self.frame_1, validate="key", validatecommand=self.vcmd1,
                                                   width=120, height=25, corner_radius=10)
        self.entry_codigo.place(relx=0.05, rely=0.15, relwidth=0.07)

        # Criação de Label e entrada de NOME
        self.lb_nome = Label(self.frame_1, text='Nome', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.entry_nome = customtkinter.CTkEntry(master=self.frame_1, width=120, height=25, corner_radius=10)
        self.entry_nome.place(relx=0.05, rely=0.45, relwidth=0.85)

        # Criação de Label e entrada de TELEFONE
        self.lb_telefone = Label(self.frame_1, text='Telefone', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_telefone.place(relx=0.05, rely=0.6)

        self.entry_telefone = customtkinter.CTkEntry(master=self.frame_1, width=120,
                                                     validate="key", validatecommand=self.vcmd2,
                                                     height=25, corner_radius=10)
        self.entry_telefone.place(relx=0.05, rely=0.7, relwidth=0.4)

        # Criação de Label e entrada de CIDADE
        self.lb_cidade = Label(self.frame_1, text='Cidade', bg='#dfe3ee', fg='#107db2', font=('verdana', 8, 'bold'))
        self.lb_cidade.place(relx=0.5, rely=0.6)

        self.entry_cidade = customtkinter.CTkEntry(master=self.frame_1, width=120, height=25, corner_radius=10)
        self.entry_cidade.place(relx=0.5, rely=0.7, relwidth=0.4)

    def lista_frame2(self):
        self.listaclientes = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4"))
        self.listaclientes.place(relx=0.01, rely=0.0128, relwidth=0.95, relheight=0.95)

        self.scroll_lista = Scrollbar(self.frame_2, orient='vertical')
        self.scroll_lista.place(relx=0.96, rely=0.0128, relwidth=0.04, relheight=0.95)

        self.listaclientes.heading("#0", text="", anchor=W)
        self.listaclientes.heading("#1", text="Codigo")
        self.listaclientes.heading("#2", text="Nome")
        self.listaclientes.heading("#3", text="Telefone")
        self.listaclientes.heading("#4", text="Cidade")

        self.listaclientes.column("#0", width=1)
        self.listaclientes.column("#1", width=50)
        self.listaclientes.column("#2", width=200)
        self.listaclientes.column("#3", width=125)
        self.listaclientes.column("#4", width=125)

        self.listaclientes.configure(yscrollcommand=self.scroll_lista.set)
        self.listaclientes.bind("<Double-1>", self.duploclick)

    def menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        menuopcao = Menu(menubar, tearoff=0)
        menurelatorio = Menu(menubar, tearoff=0)
        menubd = Menu(menubar, tearoff=0)
        menusobre = Menu(menubar, tearoff=0)

        def quit(): self.janela.destroy()

        menubar.add_cascade(label="Opções", menu=menuopcao)
        menubar.add_cascade(label="Relatorios", menu=menurelatorio)
        menubar.add_cascade(label="Manutenção", menu=menubd)
        menubar.add_cascade(label="Sobre", menu=menusobre)

        menuopcao.add_command(label="Novo")
        menuopcao.add_command(label="Pesquisar")
        menuopcao.add_command(label="Limpar Dados", command=self.limpa_tela)
        menuopcao.add_separator()
        menuopcao.add_command(label="Sair", command=quit)

        menurelatorio.add_command(label="Ficha do Cliente", command=self.gerarelatorio)

        menubd.add_command(label="Banco de Dados")

        menusobre.add_command(label="PHz Dev")

    def valida_entradas1(self):
        self.vcmd1 = (self.janela.register(self.validate_entry3), "%P")

    def valida_entradas2(self):
        self.vcmd2 = (self.janela.register(self.validate_entry2), "%P")


Aplication()
