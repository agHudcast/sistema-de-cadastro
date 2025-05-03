from flask import Flask, render_template, request, redirect, url_for, session
import json
import os

app = Flask(__name__)
app.secret_key = 'minha_chave_secreta'  # Segurança para sessão

# Função para carregar usuários
def carregar_usuarios():
    if os.path.exists('usuarios.json'):
        with open('usuarios.json', 'r') as f:
            return json.load(f)
    return []

# Função para salvar usuários
def salvar_usuarios(usuarios):
    with open('usuarios.json', 'w') as f:
        json.dump(usuarios, f, indent=4)

# Rota inicial - Login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuarios = carregar_usuarios()
        username = request.form['username']
        password = request.form['password']
        
        for usuario in usuarios:
            if usuario['usuario'] == username and usuario['senha'] == password:
                session['usuario'] = username
                return redirect(url_for('menu'))
        return "Usuário ou senha inválidos."
    return render_template('login.html')

# Rota de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        usuarios = carregar_usuarios()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        for usuario in usuarios:
            if usuario['usuario'] == username or usuario['email'] == email:
                return "Usuário ou e-mail já cadastrado."

        novo_usuario = {
            "usuario": username,
            "email": email,
            "senha": password
        }
        usuarios.append(novo_usuario)
        salvar_usuarios(usuarios)
        return redirect(url_for('login'))
    return render_template('cadastro.html')

# Rota do menu após login
@app.route('/menu')
def menu():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('menu.html', usuario=session['usuario'])

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
