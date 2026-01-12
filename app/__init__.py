from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importa e registra blueprints, modelos, etc.
    with app.app_context():
        from . import models  # Importa os modelos para criar as tabelas
        db.create_all()  # Cria as tabelas no banco de dados se não existirem
    
    return app