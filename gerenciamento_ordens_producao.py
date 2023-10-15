#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3

# Função para criar o banco de dados SQLite e a tabela de ordens de produção
def criar_banco_dados():
    conn = sqlite3.connect("ordens_producao.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_producao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            quantidade INTEGER,
            data_entrega DATE,
            status TEXT
        )
    ''')
    conn.close()

# Classe para representar uma ordem de produção
class OrdemProducao:
    def __init__(self, produto, quantidade, data_entrega, status="Em andamento"):
        self.produto = produto
        self.quantidade = quantidade
        self.data_entrega = data_entrega
        self.status = status

# Função para registrar uma nova ordem de produção
def registrar_ordem_producao():
    produto = input("Produto a ser fabricado: ")
    quantidade = int(input("Quantidade desejada: "))
    data_entrega = input("Data de entrega (YYYY-MM-DD): ")

    conn = sqlite3.connect("ordens_producao.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ordens_producao (produto, quantidade, data_entrega, status) VALUES (?, ?, ?, ?)",
                   (produto, quantidade, data_entrega, "Em andamento"))
    conn.commit()
    conn.close()

    print("Ordem de produção registrada com sucesso!")

# Função para listar todas as ordens de produção existentes
def listar_ordens_producao():
    conn = sqlite3.connect("ordens_producao.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordens_producao")
    ordens = cursor.fetchall()
    conn.close()

    if ordens:
        for ordem in ordens:
            print(f"ID: {ordem[0]}, Produto: {ordem[1]}, Quantidade: {ordem[2]}, Data de Entrega: {ordem[3]}, Status: {ordem[4]}")
    else:
        print("Nenhuma ordem de produção registrada ainda.")

# Função para atualizar o status de uma ordem de produção
def atualizar_status():
    conn = sqlite3.connect("ordens_producao.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM ordens_producao")
    ordens = cursor.fetchall()
    
    if not ordens:
        print("Nenhuma ordem de produção registrada ainda.")
        conn.close()
        return
    
    listar_ordens_producao()
    numero_ordem = int(input("Informe o ID da ordem que deseja atualizar: "))
    novo_status = input("Novo status (Em andamento / Concluída): ").capitalize()

    conn = sqlite3.connect("ordens_producao.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordens_producao WHERE id=?", (numero_ordem,))
    ordem = cursor.fetchone()

    if ordem:
        if novo_status == "Em andamento" or novo_status == "Concluída":
            cursor.execute("UPDATE ordens_producao SET status=? WHERE id=?", (novo_status, numero_ordem))
            conn.commit()
            print(f"Status da ordem {numero_ordem} atualizado com sucesso!")
        else:
            print("Status inválido. Use 'Em andamento' ou 'Concluída'.")
    else:
        print("ID de ordem inválido.")

# Função para executar o sistema
def executar_sistema():
    criar_banco_dados()

    while True:
        print("\nSistema de Gerenciamento de Ordens de Produção")
        print("1. Registrar uma nova ordem de produção")
        print("2. Listar todas as ordens de produção")
        print("3. Atualizar o status de uma ordem de produção")
        print("4. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            registrar_ordem_producao()
        elif opcao == "2":
            listar_ordens_producao()
        elif opcao == "3":
            atualizar_status()
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Escolha uma opção válida.")

if __name__ == "__main__":
    executar_sistema()

