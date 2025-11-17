from django.db import models


class Permissao(models.Model):
    descricao = models.CharField(max_length=100, unique=True)

    @staticmethod
    def criar_permissoes_padrao():
        Permissao.objects.get_or_create(descricao='Acessar área restrita')

    def __str__(self):
        return self.descricao

    class Meta:
        permissions = [
            ("acessar_area_restrita", "Pode acessar a área restrita"),
        ]
