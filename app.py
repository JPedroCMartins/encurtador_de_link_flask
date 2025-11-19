import sqlite3
import random
import string
import datetime
import os # Importa o 'os'
from flask import Flask, request, redirect, render_template, g, abort, url_for

# --- Configuração ---
app = Flask(__name__)

# Define o caminho para o diretório de dados e o arquivo do banco
DATA_DIR = 'data'
DATABASE = os.path.join(DATA_DIR, 'encurtador.db')

# --- Funções do Banco de Dados (SQLite) ---

def get_db():
    """Abre uma nova conexão com o banco de dados, se ainda não houver uma."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(
            DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        db.row_factory = sqlite3.Row 
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Fecha a conexão com o banco de dados no final da requisição."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Executa o script 'schema.sql' para criar as tabelas."""
    # Garante que a função seja chamada dentro do contexto da aplicação
    with app.app_context(): 
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# --- Lógica Principal (Sem alteração) ---

def gerar_codigo_curto(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    while True:
        codigo = ''.join(random.choices(caracteres, k=tamanho))
        db = get_db()
        cursor = db.execute('SELECT 1 FROM links WHERE codigo_curto = ?', (codigo,))
        if cursor.fetchone() is None:
            return codigo

# --- Rotas (Endpoints) (Sem alteração) ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encurtar', methods=['POST'])
def encurtar_url():
    if 'url' not in request.form:
        abort(400, "Formulário inválido. Campo 'url' não encontrado.")
    
    url_longa = request.form['url']
    codigo_curto = gerar_codigo_curto()
    data_criacao = datetime.datetime.now()
    
    db = get_db()
    db.execute(
        'INSERT INTO links (codigo_curto, url_longa, data_criacao) VALUES (?, ?, ?)',
        (codigo_curto, url_longa, data_criacao)
    )
    db.commit()
    
    url_curta_completa = url_for('redirecionar', codigo=codigo_curto, _external=True)
    
    return render_template('resultado.html', url_curta=url_curta_completa)

@app.route('/<string:codigo>')
def redirecionar(codigo):
    db = get_db()
    cursor = db.execute(
        'SELECT url_longa, data_criacao FROM links WHERE codigo_curto = ?',
        (codigo,)
    )
    link = cursor.fetchone()
    
    if link is None:
        abort(404, "URL não encontrada.")
    
    data_criacao = link['data_criacao']
    data_expiracao = data_criacao + datetime.timedelta(days=30)
    
    if datetime.datetime.now() > data_expiracao:
        db.execute('DELETE FROM links WHERE codigo_curto = ?', (codigo,))
        db.commit()
        return render_template('expirado.html'), 404
    
    return redirect(link['url_longa'])
