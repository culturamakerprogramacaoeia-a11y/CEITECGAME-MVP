from app import create_app, db
from app.models import Usuario, Turma, Missao, Recompensa

app = create_app()


# ──────────────────────────────────────────────
#  COMANDO: flask init-db
#  Cria todas as tabelas no banco de dados.
# ──────────────────────────────────────────────
@app.cli.command('init-db')
def init_db():
    """Cria todas as tabelas no banco SQLite."""
    with app.app_context():
        db.create_all()
        print('✅ Banco de dados criado com sucesso!')


# ──────────────────────────────────────────────
#  COMANDO: flask seed-db
#  Popula o banco com dados iniciais para teste.
# ──────────────────────────────────────────────
@app.cli.command('seed-db')
def seed_db():
    """Popula o banco com dados de exemplo."""
    with app.app_context():
        db.create_all()

        # Turmas
        t1 = Turma(nome='Turma Alpha', ano='2024', descricao='Turma principal de programação')
        t2 = Turma(nome='Turma Beta', ano='2024', descricao='Turma de Arduino e Maker')
        db.session.add_all([t1, t2])
        db.session.flush()  # gera IDs sem commit

        # Usuários
        admin = Usuario(nome='Admin CEITEC', email='admin@ceitec.com', tipo='admin')
        admin.set_senha('admin123')

        prof = Usuario(nome='Prof. Genezi', email='genezi@ceitec.com', tipo='professor')
        prof.set_senha('prof123')

        aluno1 = Usuario(nome='Alice Gamer', email='alice@aluno.com',
                         tipo='aluno', turma_id=t1.id)
        aluno1.set_senha('aluno123')

        aluno2 = Usuario(nome='Bruno Maker', email='bruno@aluno.com',
                         tipo='aluno', turma_id=t1.id)
        aluno2.set_senha('aluno123')

        aluno3 = Usuario(nome='Carla Code', email='carla@aluno.com',
                         tipo='aluno', turma_id=t2.id)
        aluno3.set_senha('aluno123')

        db.session.add_all([admin, prof, aluno1, aluno2, aluno3])

        # Missões
        m1 = Missao(titulo='Hello World em Python',
                    categoria='Programação', xp=50, teccoins=10,
                    descricao='Criar seu primeiro programa Python.')
        m2 = Missao(titulo='LED Piscante com Arduino',
                    categoria='Arduino', xp=80, teccoins=20,
                    descricao='Montar circuito e programar LED.')
        m3 = Missao(titulo='Projeto Maker: Suporte para Celular',
                    categoria='Maker', xp=120, teccoins=30,
                    descricao='Criar suporte utilizando materiais recicláveis.')
        m4 = Missao(titulo='Algoritmo de Busca',
                    categoria='Pensamento Computacional', xp=100, teccoins=25,
                    descricao='Implementar busca binária.')
        m5 = Missao(titulo='Loop e Condicionais',
                    categoria='Programação', xp=60, teccoins=15,
                    descricao='Exercício de lógica com for e if.')
        db.session.add_all([m1, m2, m3, m4, m5])

        # Recompensas da Loja
        r1 = Recompensa(nome='Adesivo CEITEC Exclusivo 🏷️',
                        custo_teccoins=20, nivel_minimo=1,
                        descricao='Adesivo colecionável do laboratório.')
        r2 = Recompensa(nome='Caneta Técnica 🖊️',
                        custo_teccoins=50, nivel_minimo=2,
                        descricao='Caneta especial para projetos.')
        r3 = Recompensa(nome='Kit Arduino Básico 🤖',
                        custo_teccoins=150, nivel_minimo=3,
                        descricao='Kit com componentes para projetos.')
        r4 = Recompensa(nome='Camiseta CEITEC 👕',
                        custo_teccoins=300, nivel_minimo=4,
                        descricao='Camiseta oficial do centro tecnológico.')
        db.session.add_all([r1, r2, r3, r4])

        db.session.commit()
        print('✅ Banco populado com sucesso!')
        print()
        print('══════════════════════════════════════')
        print('  CREDENCIAIS PARA TESTE:')
        print('  Admin:     admin@ceitec.com / admin123')
        print('  Professor: genezi@ceitec.com / prof123')
        print('  Aluno 1:   alice@aluno.com / aluno123')
        print('  Aluno 2:   bruno@aluno.com / aluno123')
        print('  Aluno 3:   carla@aluno.com / aluno123')
        print('══════════════════════════════════════')


if __name__ == '__main__':
    app.run(debug=True)
