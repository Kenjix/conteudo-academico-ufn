
import os
import sys
import django

def setup_django():
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()

setup_django()


from academia.models.usuario import Usuario
from academia.models.perfil import Perfil
from django.contrib.auth.models import Permission

usuarios = [
    # 8 usuários comuns
    {"username": f"usuario{i}", "email": f"usuario{i}@teste.com", "perfil_tipo": 2} for i in range(1, 9)
] + [
    # 2 instrutores
    {"username": f"instrutor{i}", "email": f"instrutor{i}@teste.com", "perfil_tipo": 1} for i in range(1, 3)
]


def main():
    # Permissões a serem atribuídas aos instrutores
    permissoes_instrutor = [
        'acessar_area_restrita',
        'aprovar_treinos',
        'cadastrar_treinos',
        'gerar_treinos',
        'remover_treinos',
    ]
    for u in usuarios:
        user = Usuario.objects.filter(username=u["username"]).first()
        if not user:
            perfil = Perfil.objects.get(tipo=u["perfil_tipo"])
            user = Usuario.objects.create_user(
                username=u["username"],
                email=u["email"],
                password="1234",
                perfil=perfil
            )
            print(f"Usuário criado: {user.username} ({'Instrutor' if u['perfil_tipo']==1 else 'Usuário'})")
        else:
            print(f"Usuário já existe: {u['username']}")
        # Se for instrutor, sempre atualiza permissões
        if u["perfil_tipo"] == 1:
            for codename in permissoes_instrutor:
                try:
                    perm = Permission.objects.get(codename=codename)
                    user.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    print(f"Permissão não encontrada: {codename}")
            print(f"Permissões de instrutor atualizadas para: {user.username}")

if __name__ == "__main__":
    main()
