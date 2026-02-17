from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Usuario, Pontuacao, Recompensa, Resgate, calcular_nivel
from .. import db
from functools import wraps

aluno_bp = Blueprint('aluno', __name__)


# ──────────────────────────────────────────────
#  DECORATOR – apenas aluno autenticado
# ──────────────────────────────────────────────
def somente_aluno(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo != 'aluno':
            flash('Área restrita a alunos.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ──────────────────────────────────────────────
#  DASHBOARD DO ALUNO
# ──────────────────────────────────────────────
@aluno_bp.route('/dashboard')
@login_required
@somente_aluno
def dashboard():
    xp = current_user.xp_total
    tc = current_user.teccoins_total
    nivel_nome, xp_min, xp_prox = calcular_nivel(xp)

    # Progresso percentual na barra (0-100)
    if xp_prox:
        progresso = int(((xp - xp_min) / (xp_prox - xp_min)) * 100)
    else:
        progresso = 100  # Mentor = nível máximo

    # Últimas 5 pontuações
    historico = (Pontuacao.query
                 .filter_by(aluno_id=current_user.id)
                 .order_by(Pontuacao.data.desc())
                 .limit(5).all())

    # Ranking da turma
    if current_user.turma_id:
        colegas = Usuario.query.filter_by(tipo='aluno', turma_id=current_user.turma_id).all()
    else:
        colegas = Usuario.query.filter_by(tipo='aluno').all()

    ranking = sorted(colegas, key=lambda a: a.xp_total, reverse=True)[:10]

    return render_template('aluno/dashboard.html',
                           xp=xp, tc=tc,
                           nivel_nome=nivel_nome,
                           xp_min=xp_min, xp_prox=xp_prox,
                           progresso=progresso,
                           historico=historico,
                           ranking=ranking,
                           calcular_nivel=calcular_nivel)


# ──────────────────────────────────────────────
#  HISTÓRICO COMPLETO DE PONTUAÇÕES
# ──────────────────────────────────────────────
@aluno_bp.route('/historico')
@login_required
@somente_aluno
def historico():
    pontuacoes = (Pontuacao.query
                  .filter_by(aluno_id=current_user.id)
                  .order_by(Pontuacao.data.desc())
                  .all())
    return render_template('aluno/historico.html', pontuacoes=pontuacoes)


# ──────────────────────────────────────────────
#  RANKING DA TURMA
# ──────────────────────────────────────────────
@aluno_bp.route('/ranking')
@login_required
@somente_aluno
def ranking():
    if current_user.turma_id:
        colegas = Usuario.query.filter_by(tipo='aluno', turma_id=current_user.turma_id).all()
    else:
        colegas = Usuario.query.filter_by(tipo='aluno').all()

    ranking_lista = sorted(colegas, key=lambda a: a.xp_total, reverse=True)
    return render_template('aluno/ranking.html',
                           ranking=ranking_lista,
                           calcular_nivel=calcular_nivel)


# ──────────────────────────────────────────────
#  LOJA – Ver recompensas
# ──────────────────────────────────────────────
@aluno_bp.route('/loja')
@login_required
@somente_aluno
def loja():
    recompensas = Recompensa.query.all()
    meus_resgates_pendentes = [r.recompensa_id for r in current_user.resgates
                                if r.status == 'pendente']
    return render_template('aluno/loja.html',
                           recompensas=recompensas,
                           meus_resgates_pendentes=meus_resgates_pendentes)


# ──────────────────────────────────────────────
#  LOJA – Solicitar resgate
# ──────────────────────────────────────────────
@aluno_bp.route('/loja/resgatar/<int:recompensa_id>', methods=['POST'])
@login_required
@somente_aluno
def resgatar(recompensa_id):
    recompensa = Recompensa.query.get_or_404(recompensa_id)

    # Verifica nível mínimo
    if current_user.nivel_numero < recompensa.nivel_minimo:
        flash('Seu nível não é suficiente para esta recompensa. 🔒', 'warning')
        return redirect(url_for('aluno.loja'))

    # Verifica TecCoins
    if current_user.teccoins_total < recompensa.custo_teccoins:
        flash('TecCoins insuficientes para este resgate. 💸', 'warning')
        return redirect(url_for('aluno.loja'))

    # Verifica se já possui resgate pendente para essa recompensa
    ja_pediu = Resgate.query.filter_by(aluno_id=current_user.id,
                                        recompensa_id=recompensa_id,
                                        status='pendente').first()
    if ja_pediu:
        flash('Você já tem um pedido pendente para essa recompensa.', 'info')
        return redirect(url_for('aluno.loja'))

    resgate = Resgate(aluno_id=current_user.id, recompensa_id=recompensa_id)
    db.session.add(resgate)
    db.session.commit()
    flash(f'Solicitação de "{recompensa.nome}" enviada! Aguarde aprovação. 🎁', 'success')
    return redirect(url_for('aluno.loja'))


# ──────────────────────────────────────────────
#  MEUS RESGATES
# ──────────────────────────────────────────────
@aluno_bp.route('/meus-resgates')
@login_required
@somente_aluno
def meus_resgates():
    resgates = (Resgate.query
                .filter_by(aluno_id=current_user.id)
                .order_by(Resgate.data.desc())
                .all())
    return render_template('aluno/meus_resgates.html', resgates=resgates)
