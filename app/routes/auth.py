from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Usuario
from .. import db

auth_bp = Blueprint('auth', __name__)


# ──────────────────────────────────────────────
#  ROTA RAIZ – redireciona para login ou dashboard
# ──────────────────────────────────────────────
@auth_bp.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.tipo in ('admin', 'professor'):
            return redirect(url_for('professor.dashboard'))
        return redirect(url_for('aluno.dashboard'))
    return redirect(url_for('auth.login'))


# ──────────────────────────────────────────────
#  LOGIN
# ──────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se já autenticado, vai para o dashboard correto
    if current_user.is_authenticated:
        return redirect(url_for('auth.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')

        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_senha(senha):
            login_user(usuario)
            flash(f'Bem-vindo(a), {usuario.nome}! 🚀', 'success')
            return redirect(url_for('auth.index'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html')


# ──────────────────────────────────────────────
#  LOGOUT
# ──────────────────────────────────────────────
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sessão encerrada com sucesso.', 'info')
    return redirect(url_for('auth.login'))
