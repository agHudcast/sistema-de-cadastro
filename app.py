from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

# Configurar o Flask
app = Flask(__name__)
app.secret_key = "chave_secreta_segura"  # Usado para mensagens flash

# Função para validar senha forte
def senha_valida(senha):
    if len(senha) < 8:
        return False

    tem_letra = False
    tem_numero = False

    for caractere in senha:
        if caractere.isalpha():
            tem_letra = True
        if caractere.isdigit():
            tem_numero = True

    return tem_letra and tem_numero

# Função para ler o arquivo de usuários
def ler_usuarios():
    if os.path.exists("usuarios.json"):
        with open("usuarios.json", "r") as f:
            return json.load(f)
    else:
        return []

# Função para salvar os usuários
def salvar_usuarios(usuarios):
    with open("usuarios.json", "w") as f:
        json.dump(usuarios, f, indent=4)

# Rota inicial: Escolher Login ou Cadastro
@app.route("/")
def index():
    return render_template("index.html")

# Rota de cadastro
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        email = request.form["email"]
        senha = request.form["senha"]
        confirmar = request.form["confirmar"]

        usuarios = ler_usuarios()

        # Confirmação de senha
        if senha != confirmar:
            flash("❌ As senhas não coincidem!", "error")
            return redirect(url_for('cadastro'))

        # Validação de senha forte
        if not senha_valida(senha):
            flash("⚠️ A senha precisa ter no mínimo 8 caracteres, uma letra e um número.", "error")
            return redirect(url_for('cadastro'))

        # Verificar se já existe usuário ou email
        for user in usuarios:
            if user['usuario'] == usuario:
                flash(f"❌ Nome de usuário '{usuario}' já existe!", "error")
                return redirect(url_for('cadastro'))
            if user['email'] == email:
                flash(f"❌ E-mail '{email}' já cadastrado!", "error")
                return redirect(url_for('cadastro'))

        novo = {
            "usuario": usuario,
            "email": email,
            "senha": senha
        }
        usuarios.append(novo)
        salvar_usuarios(usuarios)

        flash("✅ Cadastro realizado com sucesso!", "success")
        return redirect(url_for('index'))

    return render_template("cadastro.html")

# Rota de login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        usuarios = ler_usuarios()

        for user in usuarios:
            if user["usuario"] == usuario and user["senha"] == senha:
                flash(f"✅ Login bem-sucedido! Bem-vindo, {usuario}!", "success")
                return redirect(url_for('index'))

        flash("❌ Usuário ou senha incorretos!", "error")
        return redirect(url_for('login'))

    return render_template("login.html")

# Rodar a aplicação
if __name__ == "__main__":
    app.run(debug=True)