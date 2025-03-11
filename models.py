from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Setor(db.Model):
    __tablename__ = 'Setores'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'Usuarios'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Senha = db.Column(db.String(100), nullable=False)
    Tipo = db.Column(db.Enum('master', 'comum'), nullable=False, default='comum')

    def get_id(self):
        return str(self.Id)

class Veiculo(db.Model):
    __tablename__ = 'Veiculos'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Placa = db.Column(db.String(15), nullable=False, unique=True)
    Marca = db.Column(db.String(50), nullable=False)
    Status = db.Column(db.Enum('Disponível', 'Em uso', 'Manutenção'), nullable=False)

class Agendamento(db.Model):
    __tablename__ = 'Agendamentos'
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Horario_Retirada = db.Column(db.DateTime, nullable=False)
    Horario_Saida = db.Column(db.DateTime, nullable=False)
    Destino = db.Column(db.String(200), nullable=False)
    Motivo = db.Column(db.Text, nullable=False)
    idCondutor = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    idUsuario = db.Column(db.Integer, db.ForeignKey('Usuarios.Id'), nullable=False)
    idVeiculo = db.Column(db.Integer, db.ForeignKey('Veiculos.Id'), nullable=False)