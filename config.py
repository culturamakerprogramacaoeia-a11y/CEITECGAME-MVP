import os

# Diretório base da aplicação
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações gerais da aplicação."""
    # Chave secreta para sessões Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ceitecgame-secret-2024-!@#'

    # Banco de dados SQLite local
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'ceitecgame.db')

    # Desativa rastreamento de modificações (economiza memória)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
