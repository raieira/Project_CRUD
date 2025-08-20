from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

app = Flask(__name__)  #cria aplicação flask


#chave secreta usada para sessões, mensagens flash etc. (aqui uma simples para dev)
app.secret_key = "dev"


#caminho absoluto do banco de dados (garante que funcione mesmo fora da pasta atual)
DB_PATH = (Path(__file__).parent / "database.db").resolve()

# função auxiliar para abrir conexão com o banco
def get_db_connection():
    conn = sqlite3.connect(DB_PATH) #conecta ao SQlite
    conn.row_factory = sqlite3.Row  #permite acessar colunas por nome (ex: row["nome"])
    return conn

def init_db():
    if not DB_PATH.exists():
        print("[INIT_DB] Criando novo banco...")
        with get_db_connection() as conn:
            conn.executescript("""
                CREATE TABLE produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    preco REAL NOT NULL
                    );    
            """)
            conn.commit()
        print("[INIT_DB] Banco criado em: ", DB_PATH)


#rota principal ("/") que lista os produtos
@app.route("/", endpoint="home")   #"endpoit" = nome inteiro da rota
def home():
    with get_db_connection() as conn:
        produtos = conn.execute(
            "SELECT id, nome, CAST(preco AS REAL) AS preco FROM produtos ORDER BY id ASC"
        ).fetchall()
    return render_template("index.html", produtos=produtos)

    
@app.route("/add", methods=["GET", "POST"], endpoint="add")
def add_product():
    if request.method == "POST": 
        nome = (request.form.get("nome") or "").strip()
        preco_raw = (request.form.get("preco") or "").strip()

        try:
            if not nome:
                raise ValueError("nome vazio")
            preco = float(preco_raw.replace(",","."))
        except Exception:
            flash("preencha corretamente nome e preco (ex: 19.90).", "error")
            return redirect(url_for("add"))
        
        with get_db_connection() as conn:
            conn.execute("INSERT INTO produtos (nome, preco) VALUES (?,?)", (nome,preco))
            conn.commit

        flash("produto cadastrado com sucesso!","success")
        return redirect(url_for("home"))
    
    return render_template("add.html")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_product(id):
    conn = get_db_connection()
    
    produto = conn.execute(
     "SELECT * FROM produtos WHERE id = ?", (id,)
    ).fetchone()

    if not produto:
        flash("produto não encontrado!", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        nome = request.form["nome"].strip()
        preco = request.form["preco"].replace(",",".").strip()

        try:
            preco = float(preco)
            conn.execute(
                "UPDATE produtos SET nome = ?, preco = ? WHERE id = ?", (nome, preco, id) )
            conn.commit()
            flash("produto atualizado com sucesso!", "success")

        except exception:
            flash("Erro ao atualizar. verifique os dados,", "error")

        conn.close()

        return redirect(url_for("home"))

    conn.close()
    return render_template("edit.html", produto=produto)



if __name__ == "__main__":
    app.run(debug=True)