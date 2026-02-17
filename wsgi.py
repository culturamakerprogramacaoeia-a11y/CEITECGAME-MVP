import sys
import os

# Adiciona o diretório do projeto ao path
path = os.path.abspath(os.path.dirname(__file__))
if path not in sys.path:
    sys.path.append(path)

from app import create_app

application = create_app()

if __name__ == "__main__":
    application.run()
