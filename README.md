# 🔗 Encurtador de Links (Flask + UV)

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![uv](https://img.shields.io/badge/uv-Fastest_Manager-purple)
![License](https://img.shields.io/badge/License-MIT-green)

Aplicação web desenvolvida em **Flask** para encurtamento de URLs. O projeto foca em performance e simplicidade, utilizando **Gunicorn** para produção, banco de dados **SQLite** persistente e sistema de **expiração automática de links** (24 horas).

O gerenciamento de dependências é feito com `uv`, garantindo builds extremamente rápidos.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python 3.11, Flask, SQLAlchemy.
- **Banco de Dados:** SQLite (com persistência via volumes Docker).
- **Servidor:** Gunicorn (WSGI).
- **Gerenciamento de Pacotes:** [uv](https://github.com/astral-sh/uv).
- **Infraestrutura:** Docker e Docker Compose.

## ✨ Funcionalidades

- ✂️ **Encurtamento:** Gera códigos únicos de 6 caracteres.
- ⏳ **Expiração Automática:** Links são deletados automaticamente 24 horas após a criação (Lazy Deletion).
- 🐳 **Containerização:** Ambiente isolado e pronto para produção.
- 💾 **Persistência:** Dados salvos na pasta local `./data`.

## 🚀 Como Rodar

### Opção 1: Docker (Recomendado)

Esta é a forma mais simples, pois não requer instalação do Python ou `uv` na sua máquina local.

1. **Construir e subir o container:**
   ```bash
   docker compose up --build -d