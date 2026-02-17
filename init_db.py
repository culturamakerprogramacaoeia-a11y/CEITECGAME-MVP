"""
Script de inicialização do banco de dados
Popula o banco com dados iniciais para testes
"""
from app import create_app, db
from app.models import Usuario, Turma, Missao, Recompensa
from datetime import datetime

def init_database():
    """Inicializa o banco de dados com dados de exemplo"""
    app = create_app()
    
    with app.app_context():
        # Criar todas as tabelas
        print("Criando tabelas...")
        db.create_all()
        
        # Verificar se já existem dados
        if Usuario.query.first():
            print("⚠️  Banco de dados já possui dados. Abortando inicialização.")
            return
        
        print("Populando banco de dados...")
        
        # === CRIAR TURMAS ===
        turma1 = Turma(
            nome="Turma A - Manhã",
            ano=2024,
            descricao="Turma de programação básica"
        )
        turma2 = Turma(
            nome="Turma B - Tarde",
            ano=2024,
            descricao="Turma de robótica avançada"
        )
        
        db.session.add_all([turma1, turma2])
        db.session.commit()
        print("✓ Turmas criadas")
        
        # === CRIAR USUÁRIOS ===
        # Professor
        professor = Usuario(
            nome="Professor Carlos",
            email="professor@ceitec.com",
            tipo="professor"
        )
        professor.set_password("professor123")
        
        # Admin
        admin = Usuario(
            nome="Administrador",
            email="admin@ceitec.com",
            tipo="admin"
        )
        admin.set_password("admin123")
        
        # Alunos da Turma A
        aluno1 = Usuario(
            nome="Ana Silva",
            email="ana@aluno.com",
            tipo="aluno",
            turma_id=turma1.id
        )
        aluno1.set_password("aluno123")
        
        aluno2 = Usuario(
            nome="Bruno Santos",
            email="bruno@aluno.com",
            tipo="aluno",
            turma_id=turma1.id
        )
        aluno2.set_password("aluno123")
        
        aluno3 = Usuario(
            nome="Carla Oliveira",
            email="carla@aluno.com",
            tipo="aluno",
            turma_id=turma1.id
        )
        aluno3.set_password("aluno123")
        
        # Alunos da Turma B
        aluno4 = Usuario(
            nome="Daniel Costa",
            email="daniel@aluno.com",
            tipo="aluno",
            turma_id=turma2.id
        )
        aluno4.set_password("aluno123")
        
        aluno5 = Usuario(
            nome="Eduarda Lima",
            email="eduarda@aluno.com",
            tipo="aluno",
            turma_id=turma2.id
        )
        aluno5.set_password("aluno123")
        
        db.session.add_all([professor, admin, aluno1, aluno2, aluno3, aluno4, aluno5])
        db.session.commit()
        print("✓ Usuários criados")
        
        # === CRIAR MISSÕES ===
        missoes = [
            # Programação
            Missao(
                titulo="Primeiro Programa em Python",
                categoria="Programação",
                xp=50,
                teccoins=10,
                descricao="Criar um programa que exibe 'Olá, Mundo!' na tela"
            ),
            Missao(
                titulo="Calculadora Simples",
                categoria="Programação",
                xp=100,
                teccoins=20,
                descricao="Desenvolver uma calculadora com as 4 operações básicas"
            ),
            Missao(
                titulo="Jogo da Adivinhação",
                categoria="Programação",
                xp=150,
                teccoins=30,
                descricao="Criar um jogo onde o computador escolhe um número e o jogador tenta adivinhar"
            ),
            
            # Arduino
            Missao(
                titulo="LED Piscante",
                categoria="Arduino",
                xp=75,
                teccoins=15,
                descricao="Fazer um LED piscar usando Arduino"
            ),
            Missao(
                titulo="Semáforo Inteligente",
                categoria="Arduino",
                xp=120,
                teccoins=25,
                descricao="Criar um semáforo funcional com LEDs"
            ),
            Missao(
                titulo="Sensor de Temperatura",
                categoria="Arduino",
                xp=180,
                teccoins=35,
                descricao="Ler temperatura com sensor e exibir no display"
            ),
            
            # Cultura Maker
            Missao(
                titulo="Projeto de Reciclagem",
                categoria="Cultura Maker",
                xp=90,
                teccoins=18,
                descricao="Criar algo útil usando materiais reciclados"
            ),
            Missao(
                titulo="Impressão 3D Básica",
                categoria="Cultura Maker",
                xp=130,
                teccoins=26,
                descricao="Modelar e imprimir um objeto em 3D"
            ),
            
            # Pensamento Computacional
            Missao(
                titulo="Algoritmo do Dia a Dia",
                categoria="Pensamento Computacional",
                xp=60,
                teccoins=12,
                descricao="Criar um algoritmo para uma atividade cotidiana"
            ),
            Missao(
                titulo="Resolução de Problemas",
                categoria="Pensamento Computacional",
                xp=110,
                teccoins=22,
                descricao="Resolver desafios lógicos usando decomposição"
            ),
            
            # Robótica
            Missao(
                titulo="Robô Seguidor de Linha",
                categoria="Robótica",
                xp=200,
                teccoins=40,
                descricao="Construir um robô que segue uma linha preta"
            ),
            Missao(
                titulo="Braço Robótico",
                categoria="Robótica",
                xp=250,
                teccoins=50,
                descricao="Montar e programar um braço robótico"
            ),
        ]
        
        db.session.add_all(missoes)
        db.session.commit()
        print("✓ Missões criadas")
        
        # === CRIAR RECOMPENSAS ===
        recompensas = [
            Recompensa(
                nome="Adesivo CEITEC",
                custo_teccoins=50,
                descricao="Adesivo exclusivo do Centro Tecnológico",
                nivel_minimo=1
            ),
            Recompensa(
                nome="Caneta Personalizada",
                custo_teccoins=100,
                descricao="Caneta com logo do CEITEC",
                nivel_minimo=2
            ),
            Recompensa(
                nome="Camiseta Tech",
                custo_teccoins=200,
                descricao="Camiseta exclusiva para makers",
                nivel_minimo=3
            ),
            Recompensa(
                nome="Kit Arduino Básico",
                custo_teccoins=350,
                descricao="Kit com Arduino Uno e componentes básicos",
                nivel_minimo=3
            ),
            Recompensa(
                nome="Livro de Programação",
                custo_teccoins=250,
                descricao="Livro sobre Python ou JavaScript",
                nivel_minimo=2
            ),
            Recompensa(
                nome="Certificado de Destaque",
                custo_teccoins=150,
                descricao="Certificado de reconhecimento",
                nivel_minimo=2
            ),
            Recompensa(
                nome="Acesso VIP ao Lab",
                custo_teccoins=300,
                descricao="Acesso prioritário ao laboratório por 1 mês",
                nivel_minimo=4
            ),
            Recompensa(
                nome="Troféu Mentor",
                custo_teccoins=500,
                descricao="Troféu exclusivo para os melhores",
                nivel_minimo=5
            ),
        ]
        
        db.session.add_all(recompensas)
        db.session.commit()
        print("✓ Recompensas criadas")
        
        print("\n" + "="*50)
        print("✅ BANCO DE DADOS INICIALIZADO COM SUCESSO!")
        print("="*50)
        print("\n📋 CREDENCIAIS DE ACESSO:\n")
        print("👨‍🏫 PROFESSOR:")
        print("   Email: professor@ceitec.com")
        print("   Senha: professor123\n")
        print("👤 ADMIN:")
        print("   Email: admin@ceitec.com")
        print("   Senha: admin123\n")
        print("👨‍🎓 ALUNOS (todos com senha: aluno123):")
        print("   - ana@aluno.com (Turma A)")
        print("   - bruno@aluno.com (Turma A)")
        print("   - carla@aluno.com (Turma A)")
        print("   - daniel@aluno.com (Turma B)")
        print("   - eduarda@aluno.com (Turma B)")
        print("\n" + "="*50)
        print(f"📊 ESTATÍSTICAS:")
        print(f"   - {len(missoes)} missões criadas")
        print(f"   - {len(recompensas)} recompensas disponíveis")
        print(f"   - 2 turmas criadas")
        print(f"   - 7 usuários cadastrados")
        print("="*50 + "\n")

if __name__ == '__main__':
    init_database()
