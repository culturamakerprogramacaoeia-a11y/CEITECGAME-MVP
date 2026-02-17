from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models import Usuario, Turma, Missao, Pontuacao, Recompensa, Resgate, calcular_nivel
from .. import db
from datetime import datetime
from functools import wraps

professor_bp = Blueprint('professor', __name__)


# ──────────────────────────────────────────────
#  DECORATOR – apenas admin ou professor
# ──────────────────────────────────────────────
def somente_professor(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.tipo not in ('admin', 'professor'):
            flash('Acesso restrito a professores.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


# ──────────────────────────────────────────────
#  DASHBOARD PRINCIPAL
# ──────────────────────────────────────────────
@professor_bp.route('/dashboard')
@login_required
@somente_professor
def dashboard():
    total_alunos = Usuario.query.filter_by(tipo='aluno').count()
    total_missoes = Missao.query.count()
    total_pontuacoes = Pontuacao.query.count()
    resgates_pendentes = Resgate.query.filter_by(status='pendente').count()

    # Top 5 alunos por XP
    alunos = Usuario.query.filter_by(tipo='aluno').all()
    ranking = sorted(alunos, key=lambda a: a.xp_total, reverse=True)[:5]

    return render_template('professor/dashboard.html',
                           total_alunos=total_alunos,
                           total_missoes=total_missoes,
                           total_pontuacoes=total_pontuacoes,
                           resgates_pendentes=resgates_pendentes,
                           ranking=ranking,
                           calcular_nivel=calcular_nivel)


# ──────────────────────────────────────────────
#  MISSÕES – Listar
# ──────────────────────────────────────────────
@professor_bp.route('/missoes')
@login_required
@somente_professor
def listar_missoes():
    missoes = Missao.query.order_by(Missao.id.desc()).all()
    return render_template('professor/missoes.html', missoes=missoes)


# ──────────────────────────────────────────────
#  MISSÕES – Criar
# ──────────────────────────────────────────────
@professor_bp.route('/missoes/criar', methods=['GET', 'POST'])
@login_required
@somente_professor
def criar_missao():
    if request.method == 'POST':
        titulo = request.form.get('titulo', '').strip()
        categoria = request.form.get('categoria', '').strip()
        xp = int(request.form.get('xp', 0))
        teccoins = int(request.form.get('teccoins', 0))
        descricao = request.form.get('descricao', '').strip()

        if not titulo or not categoria:
            flash('Título e categoria são obrigatórios.', 'danger')
        else:
            nova = Missao(titulo=titulo, categoria=categoria,
                          xp=xp, teccoins=teccoins, descricao=descricao,
                          criado_por_id=current_user.id)
            db.session.add(nova)
            db.session.commit()
            flash(f'Missão "{titulo}" criada com sucesso! ✅', 'success')
            return redirect(url_for('professor.listar_missoes'))

    categorias = ['Programação', 'Arduino', 'Maker', 'Pensamento Computacional']
    return render_template('professor/criar_missao.html', categorias=categorias)


# ──────────────────────────────────────────────
#  MISSÕES – Excluir
# ──────────────────────────────────────────────
@professor_bp.route('/missoes/excluir/<int:missao_id>', methods=['POST'])
@login_required
@somente_professor
def excluir_missao(missao_id):
    missao = Missao.query.get_or_404(missao_id)
    db.session.delete(missao)
    db.session.commit()
    flash(f'Missão "{missao.titulo}" excluída.', 'info')
    return redirect(url_for('professor.listar_missoes'))


# ──────────────────────────────────────────────
#  ALUNOS – Listar
# ──────────────────────────────────────────────
@professor_bp.route('/alunos')
@login_required
@somente_professor
def listar_alunos():
    turma_id = request.args.get('turma_id', type=int)
    turmas = Turma.query.all()

    if turma_id:
        alunos = Usuario.query.filter_by(tipo='aluno', turma_id=turma_id).all()
    else:
        alunos = Usuario.query.filter_by(tipo='aluno').all()

    # Ordena por XP decrescente
    alunos = sorted(alunos, key=lambda a: a.xp_total, reverse=True)

    return render_template('professor/alunos.html',
                           alunos=alunos, turmas=turmas,
                           turma_selecionada=turma_id,
                           calcular_nivel=calcular_nivel)


# ──────────────────────────────────────────────
#  PONTUAÇÃO – Lançar
# ──────────────────────────────────────────────
@professor_bp.route('/lancar-pontuacao', methods=['GET', 'POST'])
@login_required
@somente_professor
def lancar_pontuacao():
    alunos = Usuario.query.filter_by(tipo='aluno').order_by(Usuario.nome).all()
    missoes = Missao.query.order_by(Missao.titulo).all()

    if request.method == 'POST':
        aluno_id = int(request.form.get('aluno_id'))
        missao_id = int(request.form.get('missao_id'))
        xp_extra = int(request.form.get('xp_extra', 0))
        teccoins_extra = int(request.form.get('teccoins_extra', 0))
        obs = request.form.get('obs', '').strip()

        aluno = Usuario.query.get(aluno_id)
        missao = Missao.query.get(missao_id)

        if not aluno or not missao:
            flash('Aluno ou missão inválidos.', 'danger')
        else:
            # XP total = XP da missão + bônus manual
            xp_final = missao.xp + xp_extra
            tc_final = missao.teccoins + teccoins_extra

            pont = Pontuacao(aluno_id=aluno_id, missao_id=missao_id,
                             xp_recebido=xp_final,
                             teccoins_recebido=tc_final,
                             obs=obs)
            db.session.add(pont)
            db.session.commit()
            flash(f'✅ {xp_final} XP e {tc_final} TecCoins lançados para {aluno.nome}!', 'success')
            return redirect(url_for('professor.lancar_pontuacao'))

    return render_template('professor/lancar_pontuacao.html',
                           alunos=alunos, missoes=missoes)


# ──────────────────────────────────────────────
#  RANKING GERAL
# ──────────────────────────────────────────────
@professor_bp.route('/ranking')
@login_required
@somente_professor
def ranking():
    alunos = Usuario.query.filter_by(tipo='aluno').all()
    ranking_lista = sorted(alunos, key=lambda a: a.xp_total, reverse=True)
    return render_template('professor/ranking.html',
                           ranking=ranking_lista,
                           calcular_nivel=calcular_nivel)


# ──────────────────────────────────────────────
#  RESGATES – Gerenciar
# ──────────────────────────────────────────────
@professor_bp.route('/resgates')
@login_required
@somente_professor
def gerenciar_resgates():
    resgates = Resgate.query.order_by(Resgate.data.desc()).all()
    return render_template('professor/resgates.html', resgates=resgates)


@professor_bp.route('/resgates/<int:resgate_id>/aprovar', methods=['POST'])
@login_required
@somente_professor
def aprovar_resgate(resgate_id):
    resgate = Resgate.query.get_or_404(resgate_id)
    resgate.status = 'aprovado'
    db.session.commit()
    flash('Resgate aprovado! ✅', 'success')
    return redirect(url_for('professor.gerenciar_resgates'))


@professor_bp.route('/resgates/<int:resgate_id>/recusar', methods=['POST'])
@login_required
@somente_professor
def recusar_resgate(resgate_id):
    resgate = Resgate.query.get_or_404(resgate_id)
    resgate.status = 'recusado'
    db.session.commit()
    flash('Resgate recusado.', 'warning')
    return redirect(url_for('professor.gerenciar_resgates'))


# ──────────────────────────────────────────────
#  RECOMPENSAS – Gerenciar
# ──────────────────────────────────────────────
@professor_bp.route('/recompensas')
@login_required
@somente_professor
def listar_recompensas():
    recompensas = Recompensa.query.all()
    return render_template('professor/recompensas.html', recompensas=recompensas)


@professor_bp.route('/recompensas/criar', methods=['GET', 'POST'])
@login_required
@somente_professor
def criar_recompensa():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        custo = int(request.form.get('custo_teccoins', 0))
        descricao = request.form.get('descricao', '').strip()
        nivel_min = int(request.form.get('nivel_minimo', 1))

        if not nome:
            flash('Nome da recompensa é obrigatório.', 'danger')
        else:
            r = Recompensa(nome=nome, custo_teccoins=custo,
                           descricao=descricao, nivel_minimo=nivel_min)
            db.session.add(r)
            db.session.commit()
            flash(f'Recompensa "{nome}" criada! 🎁', 'success')
            return redirect(url_for('professor.listar_recompensas'))

    niveis = [
        (1, 'Explorador'), (2, 'Programador'),
        (3, 'Maker'), (4, 'Engenheiro'), (5, 'Mentor')
    ]
    return render_template('professor/criar_recompensa.html', niveis=niveis)


# ──────────────────────────────────────────────
#  GERENCIAR ALUNOS – Criar novo aluno
# ──────────────────────────────────────────────
@professor_bp.route('/alunos/criar', methods=['GET', 'POST'])
@login_required
@somente_professor
def criar_aluno():
    turmas = Turma.query.all()
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        email = request.form.get('email', '').strip().lower()
        senha = request.form.get('senha', '')
        turma_id = request.form.get('turma_id', type=int)

        if Usuario.query.filter_by(email=email).first():
            flash('Email já cadastrado.', 'danger')
        elif not nome or not email or not senha:
            flash('Preencha todos os campos obrigatórios.', 'danger')
        else:
            aluno = Usuario(nome=nome, email=email, tipo='aluno', turma_id=turma_id)
            aluno.set_senha(senha)
            db.session.add(aluno)
            db.session.commit()
            flash(f'Aluno {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('professor.listar_alunos'))

    return render_template('professor/criar_aluno.html', turmas=turmas)


# ──────────────────────────────────────────────
#  TURMAS – Listar
# ──────────────────────────────────────────────
@professor_bp.route('/turmas')
@login_required
@somente_professor
def listar_turmas():
    turmas = Turma.query.all()
    return render_template('professor/turmas.html', turmas=turmas)


# ──────────────────────────────────────────────
#  TURMAS – Criar
# ──────────────────────────────────────────────
@professor_bp.route('/turmas/criar', methods=['GET', 'POST'])
@login_required
@somente_professor
def criar_turma():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        ano = request.form.get('ano', '').strip()
        descricao = request.form.get('descricao', '').strip()

        if not nome or not ano:
            flash('Nome e ano da turma são obrigatórios.', 'danger')
        else:
            nova = Turma(nome=nome, ano=ano, descricao=descricao)
            db.session.add(nova)
            db.session.commit()
            flash(f'Turma "{nome}" criada com sucesso! ✅', 'success')
            return redirect(url_for('professor.listar_turmas'))

    return render_template('professor/criar_turma.html')


# ──────────────────────────────────────────────
#  TURMAS – Excluir
# ──────────────────────────────────────────────
@professor_bp.route('/turmas/excluir/<int:turma_id>', methods=['POST'])
@login_required
@somente_professor
def excluir_turma(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    # Verifica se há alunos vinculados
    if Usuario.query.filter_by(turma_id=turma_id).first():
        flash(f'Não é possível excluir a turma "{turma.nome}" pois ela possui alunos vinculados.', 'danger')
    else:
        db.session.delete(turma)
        db.session.commit()
        flash(f'Turma "{turma.nome}" excluída.', 'info')
    return redirect(url_for('professor.listar_turmas'))

