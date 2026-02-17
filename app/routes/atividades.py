from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..models import Usuario, Pontuacao, Missao, db
from functools import wraps
import json

atividades_bp = Blueprint('atividades', __name__)

def acesso_atividades(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        # Permitir alunos, professores e admins
        if current_user.tipo not in ('aluno', 'professor', 'admin'):
            flash('Área restrita.', 'danger')
            return redirect(url_for('auth.index'))
        return f(*args, **kwargs)
    return decorated

@atividades_bp.route('/')
@login_required
@acesso_atividades
def menu():
    return render_template('aluno/atividades/menu.html')

@atividades_bp.route('/matematica')
@login_required
@acesso_atividades
def matematica():
    return render_template('aluno/atividades/matematica.html')

@atividades_bp.route('/empreendedorismo')
@login_required
@acesso_atividades
def empreendedorismo():
    return render_template('aluno/atividades/empreendedorismo.html')

@atividades_bp.route('/save', methods=['POST'])
@login_required
@acesso_atividades
def save_result():
    data = request.get_json()
    tipo = data.get('tipo') 
    xp = data.get('xp', 0)
    teccoins = data.get('teccoins', 0)
    obs = data.get('obs', 'Atividade concluída com sucesso!')

    missao_nome = f"Atividade Online: {tipo.capitalize()}"
    missao = Missao.query.filter_by(titulo=missao_nome).first()
    
    if not missao:
        missao = Missao(
            titulo=missao_nome,
            categoria="Atividade Online",
            xp=0, 
            teccoins=0,
            descricao=f"Atividades interativas de {tipo} realizadas no portal."
        )
        db.session.add(missao)
        db.session.commit()

    nova_pontuacao = Pontuacao(
        aluno_id=current_user.id,
        missao_id=missao.id,
        xp_recebido=xp,
        teccoins_recebido=teccoins,
        obs=obs
    )
    
    db.session.add(nova_pontuacao)
    db.session.commit()

    return jsonify({
        "status": "success", 
        "message": f"Você ganhou {xp} XP e {teccoins} TecCoins!",
        "new_xp": current_user.xp_total,
        "new_tc": current_user.teccoins_total
    })
