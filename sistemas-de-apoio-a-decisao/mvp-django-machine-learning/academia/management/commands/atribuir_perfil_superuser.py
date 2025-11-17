from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from academia.models.perfil import Perfil

class Command(BaseCommand):
    help = 'Atribui o perfil padrão (Usuário) a todos os superusuários sem perfil.'

    def handle(self, *args, **options):
        User = get_user_model()
        perfil_usuario = Perfil.objects.get(tipo=2)  # 2 = Usuário
        superusers = User.objects.filter(is_superuser=True, perfil__isnull=True)
        for user in superusers:
            user.perfil = perfil_usuario
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Perfil atribuído ao superusuário: {user.username}'))
        if not superusers:
            self.stdout.write(self.style.WARNING('Nenhum superusuário sem perfil encontrado.'))
