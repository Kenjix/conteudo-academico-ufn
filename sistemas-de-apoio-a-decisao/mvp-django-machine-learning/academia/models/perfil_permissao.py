from django.db import models
from .perfil import Perfil
from .permissao import Permissao

class PerfilPermissao(models.Model):
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE)
    permissao = models.ForeignKey(Permissao, on_delete=models.CASCADE)
