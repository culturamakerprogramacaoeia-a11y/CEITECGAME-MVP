from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


# ──────────────────────────────────────────────
#  FUNÇÃO UTILITÁRIA – Cálculo de Nível por XP
# ──────────────────────────────────────────────
def calcular_nivel(xp_total):
    """
    Retorna (nome_do_nivel, xp_minimo, xp_proximo) com base no XP acumulado.
    O nível NUNCA é armazenado no banco; sempre calculado dinamicamente.
    """
    if xp_total >= 1000:
        return ("Mentor", 1000, None)
    elif xp_total >= 601:
        return ("Engenheiro", 601, 1000)
    elif xp_total >= 301:
        return ("Maker", 301, 601)
    elif xp_total >= 101:
        return ("Programador", 101, 301)
    else:
        return ("Explorador", 0, 101)


# ──────────────────────────────────────────────
#  MODELO: Turma
# ──────────────────────────────────────────────
class Turma(db.Model):
    __tablename__ = 'turma'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    ano = db.Column(db.String(10), nullable=False)
    descricao = db.Column(db.Text, default='')

    # Relação: uma turma possui vários usuários
    usuarios = db.relationship('Usuario', backref='turma', lazy=True)

    def __repr__(self):
        return f'<Turma {self.nome} - {self.ano}>'


# ──────────────────────────────────────────────
#  MODELO: Usuario (Professor / Aluno / Admin)
# ──────────────────────────────────────────────
class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    # tipo: 'admin', 'professor', 'aluno'
    tipo = db.Column(db.String(20), nullable=False, default='aluno')
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)

    # Relações
    pontuacoes = db.relationship('Pontuacao', backref='aluno', lazy=True,
                                  foreign_keys='Pontuacao.aluno_id')
    resgates = db.relationship('Resgate', backref='aluno', lazy=True,
                                foreign_keys='Resgate.aluno_id')

    def set_senha(self, senha):
        """Gera hash da senha antes de salvar."""
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha):
        """Verifica se a senha informada corresponde ao hash."""
        return check_password_hash(self.senha_hash, senha)

    @property
    def xp_total(self):
        """Soma todos os XP recebidos pelo aluno."""
        return sum(p.xp_recebido for p in self.pontuacoes)

    @property
    def teccoins_total(self):
        """Soma todas as TecCoins recebidas menos as gastas em resgates aprovados."""
        ganhas = sum(p.teccoins_recebido for p in self.pontuacoes)
        gastas = sum(
            r.recompensa.custo_teccoins for r in self.resgates
            if r.status == 'aprovado'
        )
        return ganhas - gastas

    @property
    def nivel(self):
        """Retorna o nome do nível atual."""
        return calcular_nivel(self.xp_total)[0]

    @property
    def nivel_numero(self):
        """Retorna um índice numérico do nível (para comparação com nivel_minimo)."""
        mapa = {"Explorador": 1, "Programador": 2, "Maker": 3,
                "Engenheiro": 4, "Mentor": 5}
        return mapa.get(self.nivel, 1)

    def __repr__(self):
        return f'<Usuario {self.nome} [{self.tipo}]>'


# ──────────────────────────────────────────────
#  MODELO: Missao
# ──────────────────────────────────────────────
class Missao(db.Model):
    __tablename__ = 'missao'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    # categoria: 'Programação', 'Arduino', 'Maker', 'Pensamento Computacional'
    categoria = db.Column(db.String(100), nullable=False)
    xp = db.Column(db.Integer, nullable=False, default=0)
    teccoins = db.Column(db.Integer, nullable=False, default=0)
    descricao = db.Column(db.Text, default='')
    criado_por_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=True)

    # Relação: uma missão pode ter várias pontuações lançadas
    pontuacoes = db.relationship('Pontuacao', backref='missao', lazy=True)

    def __repr__(self):
        return f'<Missao {self.titulo}>'


# ──────────────────────────────────────────────
#  MODELO: Pontuacao
# ──────────────────────────────────────────────
class Pontuacao(db.Model):
    __tablename__ = 'pontuacao'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    missao_id = db.Column(db.Integer, db.ForeignKey('missao.id'), nullable=False)
    xp_recebido = db.Column(db.Integer, nullable=False, default=0)
    teccoins_recebido = db.Column(db.Integer, nullable=False, default=0)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    # Observação opcional do professor
    obs = db.Column(db.Text, default='')

    def __repr__(self):
        return f'<Pontuacao aluno={self.aluno_id} missao={self.missao_id}>'


# ──────────────────────────────────────────────
#  MODELO: Recompensa (Loja)
# ──────────────────────────────────────────────
class Recompensa(db.Model):
    __tablename__ = 'recompensa'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    custo_teccoins = db.Column(db.Integer, nullable=False, default=0)
    descricao = db.Column(db.Text, default='')
    # nivel_minimo: 1=Explorador … 5=Mentor
    nivel_minimo = db.Column(db.Integer, nullable=False, default=1)

    resgates = db.relationship('Resgate', backref='recompensa', lazy=True)

    def __repr__(self):
        return f'<Recompensa {self.nome}>'


# ──────────────────────────────────────────────
#  MODELO: Resgate
# ──────────────────────────────────────────────
class Resgate(db.Model):
    __tablename__ = 'resgate'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    recompensa_id = db.Column(db.Integer, db.ForeignKey('recompensa.id'), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    # status: 'pendente', 'aprovado', 'recusado'
    status = db.Column(db.String(20), nullable=False, default='pendente')

    def __repr__(self):
        return f'<Resgate aluno={self.aluno_id} recompensa={self.recompensa_id} status={self.status}>'
