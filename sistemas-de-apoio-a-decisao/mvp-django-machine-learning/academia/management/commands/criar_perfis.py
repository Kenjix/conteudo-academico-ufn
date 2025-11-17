from django.core.management.base import BaseCommand
from academia.models.perfil import Perfil

class Command(BaseCommand):
    help = 'Cria perfis padrão: Instrutor e Usuário'

    def handle(self, *args, **options):
        created = []
        for tipo, _ in Perfil.Tipo.choices:
            obj, was_created = Perfil.objects.get_or_create(tipo=tipo)
            if was_created:
                created.append(obj.descricao)
        if created:
            self.stdout.write(self.style.SUCCESS(f'Perfis criados: {", ".join(created)}'))
        else:
            self.stdout.write(self.style.WARNING('Perfis já existem.'))
