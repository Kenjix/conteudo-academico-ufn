from django.contrib.auth.models import AbstractUser
from django.db import models
from .perfil import Perfil

class Usuario(AbstractUser):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, default=2)
    peso = models.FloatField(null=True, blank=True)
    altura = models.FloatField(null=True, blank=True)
    sexo = models.CharField(max_length=10, null=True, blank=True)
    experiencia = models.CharField(max_length=100, null=True, blank=True)
    # Objetivo do usuário (ex: emagrecimento, resistencia, reabilitacao, musculacao)
    OBJETIVO_CHOICES = [
        ('emagrecimento', 'Emagrecimento'),
        ('resistencia', 'Resistência'),
        ('reabilitacao', 'Reabilitação'),
        ('musculacao', 'Musculação'),
    ]
    objetivo = models.CharField(max_length=50, choices=OBJETIVO_CHOICES, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
