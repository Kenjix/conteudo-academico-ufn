from django.db import models

class Perfil(models.Model):
    class Tipo(models.IntegerChoices):
        INSTRUTOR = 1, 'Instrutor'
        USUARIO = 2, 'Usuário'

    tipo = models.IntegerField(choices=Tipo.choices, unique=True)

    @property
    def descricao(self):
        return self.get_tipo_display()

    def __str__(self):
        return self.descricao
