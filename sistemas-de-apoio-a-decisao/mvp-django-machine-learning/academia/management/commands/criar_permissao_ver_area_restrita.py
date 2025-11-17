from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from academia.models.permissao import Permissao

class Command(BaseCommand):
    help = 'Cria a permissão acessar_area_restrita (Django Permission) para acesso à área restrita.'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(Permissao)
        perm_codename = 'acessar_area_restrita'
        perm_name = 'Pode acessar a área restrita'
        perm, created = Permission.objects.get_or_create(
            codename=perm_codename,
            content_type=content_type,
            defaults={'name': perm_name}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Permissão "{perm_codename}" criada com sucesso.'))
        else:
            self.stdout.write(self.style.WARNING(f'Permissão "{perm_codename}" já existe.'))
