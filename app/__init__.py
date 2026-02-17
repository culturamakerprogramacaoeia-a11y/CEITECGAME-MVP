from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instâncias globais (sem app ainda – padrão Application Factory)
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Factory function: cria e configura a aplicação Flask."""
    app = Flask(__name__)

    # Carrega configurações do config.py na raiz do projeto
    app.config.from_object('config.Config')

    # Inicializa extensões
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'          # rota de login
    login_manager.login_message = 'Por favor, faça login para acessar.'
    login_manager.login_message_category = 'warning'

    # Registra blueprints
    from .routes.auth import auth_bp
    from .routes.professor import professor_bp
    from .routes.aluno import aluno_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(professor_bp, url_prefix='/professor')
    app.register_blueprint(aluno_bp, url_prefix='/aluno')

    return app


@login_manager.user_loader
def load_user(user_id):
    """Callback do Flask-Login: carrega usuário pelo id da sessão."""
    from .models import Usuario
    return Usuario.query.get(int(user_id))
