from django.core.management.base import BaseCommand
from academia.models.treino import Treino

TREINOS = [
    {"nome": "Treino A (Peito, Triceps, Ombro)", "objetivo": "emagrecimento", "nivel_experiencia": "iniciante", "descricao": "Treino para peito, triceps e ombro."},
    {"nome": "Treino B (Costas, Biceps, Abdomen)", "objetivo": "resistencia", "nivel_experiencia": "intermediario", "descricao": "Treino para costas, biceps e abdomen."},
    {"nome": "Treino C (Pernas Completo)", "objetivo": "musculacao", "nivel_experiencia": "avancado", "descricao": "Treino completo de pernas."},
    {"nome": "Treino D (Funcional / Reabilitacao)", "objetivo": "reabilitacao", "nivel_experiencia": "iniciante", "descricao": "Treino funcional para reabilitacao."},
]

class Command(BaseCommand):
    help = 'Popula treinos de teste para o modelo NN'

    def handle(self, *args, **kwargs):
        for t in TREINOS:
            treino, created = Treino.objects.get_or_create(
                nome=t["nome"],
                defaults={
                    "objetivo": t["objetivo"],
                    "nivel_experiencia": t["nivel_experiencia"],
                    "descricao": t["descricao"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Treino criado: {treino.nome}'))
            else:
                self.stdout.write(self.style.WARNING(f'Treino já existe: {treino.nome}'))
