from django.db import models
from .exercicio import Exercicio
from .equipamento import Equipamento

class ExercEquip(models.Model):
    exercicio = models.ForeignKey(Exercicio, on_delete=models.CASCADE)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Exercício Realizado'
        verbose_name_plural = 'Exercícios Realizados'
