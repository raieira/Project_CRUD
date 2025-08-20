import sqlite3 #inporta a biblioteca padrão do python para trabalhar com SQlite

#Conecta (ou cria) o arquivo do banco de dados chamado 'database'db.
#Se o arquivo não existir, ele será criado automaticamente

conn = sqlite3.connect('database.db')

#criar um cursor, que é p "controlador" para executar comandos SQL no banco
c = conn.cursor()

#executa o comando SQL para criar a tabela "produtos"
# - id: indentificador unico, numerico autoincremental
# - nome: camop de texto obrigatorio
# - preco: campo numerico decimal obrigatorio
c.execute('''
CREATE TABLE produtos (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          nome TEXT NOT NULL,
          preco REAL NOT NULL
          )
          ''')

# salva (confirma) as alterações feitas no banco
conn.commit()

# fecha a conexão com banco, liberando recursos
conn.close()