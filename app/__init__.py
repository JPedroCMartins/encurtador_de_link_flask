import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Garante que o caminho absoluto para o banco seja usado corretamente
    base_dir = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(os.path.dirname(base_dir), 'data')
    
    # Cria a pasta data se não existir
    os.makedirs(data_dir, exist_ok=True)

    # Configurações do banco de dados
    db_path = os.path.join(data_dir, 'database.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Importa e registra blueprints e modelos
    from . import models  # Importa os modelos para o contexto
    
    # Registra as rotas (Blueprint)
    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()  # Cria tabelas iniciais (útil para dev)
    
    return app