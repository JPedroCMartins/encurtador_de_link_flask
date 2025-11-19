# 1. Imagem base
FROM python:3.10-slim

# 2. Define o diretório de trabalho
WORKDIR /app

# 3. Copia e instala as dependências (agora com gunicorn)
COPY requirements.txt .
RUN pip install -r requirements.txt

# 5. Copia todo o resto do projeto
COPY . .

# 6. Expõe a porta 5000
EXPOSE 8002

# 7. O comando de produção
#    Usamos 'sh -c' para rodar múltiplos comandos:
#    Primeiro, o 'python init_db.py' para garantir que o DB exista.
#    Se ele for bem-sucedido (&&), inicia o Gunicorn.
CMD ["sh", "-c", "python init_db.py && gunicorn --workers 4 --bind 0.0.0.0:8002 app:app"]