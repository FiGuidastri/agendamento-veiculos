from functools import wraps
from flask import Flask, request, jsonify, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from models import db, Setor, Usuario, Veiculo, Agendamento
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config  # Importa as configurações

app = Flask(__name__)

# Carrega as configurações do arquivo config.py
app.config.from_object(Config)

# Inicializa o SQLAlchemy e o LoginManager
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Função para verificar se o usuário é "master"
def master_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'master':
            return jsonify({"error": "Acesso negado. Permissão insuficiente."}), 403
        return f(*args, **kwargs)
    return decorated_function

# Rotas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(Email=email).first()
        if usuario and check_password_hash(usuario.Senha, senha):
            login_user(usuario)
            return redirect(url_for('index'))
        else:
            return jsonify({"error": "Email ou senha incorretos."}), 401

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/criar_usuario', methods=['GET', 'POST'])
@master_required
def criar_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        tipo = request.form.get('tipo')

        if tipo not in ['master', 'comum']:
            return jsonify({"error": "Tipo de usuário inválido."}), 400

        senha_hash = generate_password_hash(senha)
        novo_usuario = Usuario(Nome=nome, Email=email, Senha=senha_hash, Tipo=tipo)
        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({"message": "Usuário criado com sucesso!", "id": novo_usuario.Id}), 201

    return render_template('criar_usuario.html')

@app.route('/adicionar_veiculo', methods=['GET', 'POST'])
@master_required
def adicionar_veiculo():
    if request.method == 'POST':
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        status = request.form.get('status')

        if status not in ['Disponível', 'Em uso', 'Manutenção']:
            return jsonify({"error": "Status do veículo inválido."}), 400

        novo_veiculo = Veiculo(Placa=placa, Marca=marca, Status=status)
        db.session.add(novo_veiculo)
        db.session.commit()

        return jsonify({"message": "Veículo adicionado com sucesso!", "id": novo_veiculo.Id}), 201

    return render_template('adicionar_veiculo.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, se não existirem
    app.run(debug=True)