import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from academia.models.treino import Treino, Objetivo

def populate_treinos():
    treinos_data = [
        {
            'nome': 'Treino A (Peito, Triceps, Ombro)',
            'objetivo': 'musculacao',
            'nivel_experiencia': 'intermediario',
            'descricao': 'Foco em hipertrofia para peito, tríceps e ombros. 3 séries de 8-12 reps.'
        },
        {
            'nome': 'Treino B (Costas, Biceps, Abdomen)',
            'objetivo': 'musculacao',
            'nivel_experiencia': 'intermediario',
            'descricao': 'Treino para costas, bíceps e core. Inclui exercícios compostos e isolados.'
        },
        {
            'nome': 'Treino C (Pernas Completo)',
            'objetivo': 'musculacao',
            'nivel_experiencia': 'avancado',
            'descricao': 'Treino intenso para pernas: agachamentos, leg press, extensões e flexões.'
        },
        {
            'nome': 'Treino D (Funcional / Reabilitacao)',
            'objetivo': 'reabilitacao',
            'nivel_experiencia': 'iniciante',
            'descricao': 'Exercícios funcionais leves para reabilitação e mobilidade.'
        },
        {
            'nome': 'Treino E (Cardio e Força)',
            'objetivo': 'resistencia',
            'nivel_experiencia': 'intermediario',
            'descricao': 'Combinação de cardio e força para melhorar resistência cardiovascular.'
        },
        {
            'nome': 'Treino F (Full Body)',
            'objetivo': 'emagrecimento',
            'nivel_experiencia': 'iniciante',
            'descricao': 'Treino completo para queima calórica e tonificação geral.'
        },
        {
            'nome': 'Treino G (HIIT)',
            'objetivo': 'emagrecimento',
            'nivel_experiencia': 'avancado',
            'descricao': 'Treino intervalado de alta intensidade para máxima queima de gordura.'
        },
        {
            'nome': 'Treino H (Yoga e Flexibilidade)',
            'objetivo': 'reabilitacao',
            'nivel_experiencia': 'iniciante',
            'descricao': 'Sessões de yoga para melhorar flexibilidade e reduzir estresse.'
        },
    ]

    for data in treinos_data:
        Treino.objects.get_or_create(
            nome=data['nome'],
            defaults={
                'objetivo': data['objetivo'],
                'nivel_experiencia': data['nivel_experiencia'],
                'descricao': data['descricao']
            }
        )
        print(f"Treino '{data['nome']}' criado ou já existe.")

if __name__ == '__main__':
    populate_treinos()
    print("População de treinos concluída!")