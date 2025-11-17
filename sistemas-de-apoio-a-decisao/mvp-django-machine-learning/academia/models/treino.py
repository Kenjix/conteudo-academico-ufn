from django.db import models
from django.conf import settings
from .exercicio import Exercicio


class Objetivo(models.TextChoices):
    EMAGRECIMENTO = 'emagrecimento', 'Emagrecimento'
    RESISTENCIA = 'resistencia', 'Resistência'
    REABILITACAO = 'reabilitacao', 'Reabilitação'
    HIPERTROFIA = 'hipertrofia', 'Hipertrofia'


class Treino(models.Model):
    nome = models.CharField(max_length=200, blank=True, default='')
    objetivo = models.CharField(max_length=50, choices=Objetivo.choices)
    nivel_experiencia = models.CharField(max_length=50, blank=True, null=True)  # 'iniciante', 'intermediario', 'avancado'
    descricao = models.TextField(blank=True)
    exercicios = models.ManyToManyField(Exercicio, through='TreinoExercicio')

    def __str__(self):
        return f"{self.nome} ({self.get_objetivo_display()})"


class TreinoExercicio(models.Model):
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(default=1)
    series = models.CharField(max_length=50, blank=True)
    repeticoes = models.CharField(max_length=50, blank=True)
    intensidade = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['ordem']


class PlanoTreino(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='planos')
    treino = models.ForeignKey(Treino, on_delete=models.CASCADE)
    objetivo = models.CharField(max_length=50, choices=Objetivo.choices)
    frequencia_semanal = models.PositiveIntegerField(default=3)
    duracao_semanas = models.PositiveIntegerField(default=8)
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='planos_criados')
    aprovado = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plano {self.treino.nome} para {self.usuario.username}"
