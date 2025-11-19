import os
# Importa as variáveis e funções necessárias do nosso app.py
from app import app, init_db, DATABASE, DATA_DIR

print("Verificando banco de dados para produção...")

# 1. Garante que o diretório 'data' exista
os.makedirs(DATA_DIR, exist_ok=True)

# 2. Verifica se o arquivo do banco de dados NÃO existe
if not os.path.exists(DATABASE):
    print(f"Banco de dados não encontrado em '{DATABASE}'. Criando...")
    
    # Precisamos do "contexto" da aplicação para acessar o DB
    with app.app_context():
        init_db()
        
    print("Banco de dados inicializado com sucesso.")
else:
    print(f"Banco de dados encontrado em '{DATABASE}'.")

print("Verificação do banco de dados concluída.")