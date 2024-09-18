import sqlite3
import datetime
from tkinter import messagebox


conn = sqlite3.connect('Z:/Diversos/Projetos T.I/Rizoma/DeParaRizoma.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS dePara (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    DE TEXT NOT NULL,
    PARA TEXT NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS CliFor (
    DESCRICAO TEXT NOT NULL PRIMARY KEY,
    CONTA TEXT NOT NULL
)
''')

def adicionar_Dados(DE, PARA):
    # Verificar se o par DE e PARA já existe no banco de dados
    cursor.execute('SELECT * FROM dePara WHERE DE = ? AND PARA = ?', (DE, PARA))
    resultado = cursor.fetchone()  # Pega o primeiro resultado, se existir

    if resultado:
        # Se já existir, perguntar se deseja atualizar
        resposta = messagebox.askquestion("Atualizar", "Essa associação DE-PARA já existe. Deseja atualizar os dados?", icon='warning')

        if resposta == 'yes':
            # Atualizar os dados no banco de dados
            cursor.execute('UPDATE dePara SET PARA = ? WHERE DE = ?', (PARA, DE))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Os dados não foram atualizados.")
    else:
        # Se não existir, insere os novos dados
        cursor.execute('INSERT INTO dePara(DE, PARA) VALUES (?, ?)', (DE, PARA))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Dados do histórico: {DE} cadastrados com sucesso!")
def adicionar_CliFor(DESCRICAO, CONTA):
    # Verificar se a descrição e a conta já existem no banco de dados
    cursor.execute('SELECT * FROM CliFor WHERE DESCRICAO = ? AND CONTA = ?', (DESCRICAO, CONTA))
    resultado = cursor.fetchone()

    if resultado:
        # Se já existir, perguntar se deseja atualizar
        resposta = messagebox.askquestion("Atualizar", "Esse cliente/Fornecedor já existe. Deseja atualizar os dados?", icon='warning')

        if resposta == 'yes':
            # Atualizar os dados existentes no banco de dados
            cursor.execute('UPDATE CliFor SET CONTA = ? WHERE DESCRICAO = ?', (CONTA, DESCRICAO))
            conn.commit()
            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")
        else:
            messagebox.showinfo("Aviso", "Os dados não foram atualizados.")
    else:
        # Se não existir, inserir os novos dados
        cursor.execute('INSERT INTO CliFor(DESCRICAO, CONTA) VALUES (?, ?)', (DESCRICAO, CONTA))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Dados do {DESCRICAO} cadastrados com sucesso!")
def ConsultarCliente(valor):
    cursor.execute('SELECT * FROM CliFor')
    tabelaClientes = cursor.fetchall()

    if tabelaClientes:
        # Modificando a consulta para ser case-insensitive
        cursor.execute('SELECT DESCRICAO, CONTA FROM CliFor WHERE LOWER(DESCRICAO) = LOWER(?)', (valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][1]
        else:
            return f"6"
    else:
        return f"6"
def ConsultarHistorico(valor):
    cursor.execute('SELECT * FROM dePara')
    tabelaHistorico = cursor.fetchall()

    if tabelaHistorico:
        # Realiza a consulta diretamente sem LOWER
        cursor.execute('SELECT DE, PARA FROM dePara WHERE ? LIKE "%" || DE || "%" COLLATE NOCASE', (valor,))
        tabela = cursor.fetchall()
        if tabela:
            return tabela[0][1]
        else:
            return f"6"
    else:
        return f"6"