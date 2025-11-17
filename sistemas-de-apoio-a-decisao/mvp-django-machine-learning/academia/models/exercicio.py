from django.db import models
from .equipamento import Equipamento

class Exercicio(models.Model):
    descricao = models.CharField(max_length=100)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.descricao
