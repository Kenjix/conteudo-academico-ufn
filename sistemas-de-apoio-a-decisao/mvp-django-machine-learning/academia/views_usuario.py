
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.models import Permission
from .models.perfil_permissao import PerfilPermissao
from .models.perfil import Perfil
from .models.treino import PlanoTreino, Treino
from django.contrib.auth import get_user_model, update_session_auth_hash

@login_required
def meus_treinos(request):
    if request.user.has_perm('academia.acessar_area_restrita'):
        # Instrutor vê todos os planos aprovados
        planos = PlanoTreino.objects.filter(aprovado=True).select_related('usuario', 'treino')
    else:
        # Usuário vê apenas os seus
        planos = request.user.planos.filter(aprovado=True).select_related('treino')
    return render(request, 'usuarios/meus_treinos.html', {'planos': planos})

# Permissão CRUD (após os imports)
class PermissaoForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']

@login_required
@permission_required('academia.acessar_area_restrita', raise_exception=True)
@permission_required('auth.gerenciar_permissoes', raise_exception=True)
def gerenciar_permissoes(request):
    from django.contrib.contenttypes.models import ContentType
    # Criar a permissão customizada para gerenciar permissoes se não existir
    content_type = ContentType.objects.get_for_model(Permission)
    perm_gerenciar_permissoes, created = Permission.objects.get_or_create(
        codename='gerenciar_permissoes',
        defaults={'name': 'Pode gerenciar permissões', 'content_type': content_type}
    )
    # Criar a permissão customizada para aprovar treinos se não existir
    content_type_plano = ContentType.objects.get_for_model(PlanoTreino)
    perm_aprovar, created = Permission.objects.get_or_create(
        codename='aprovar_treinos',
        defaults={'name': 'Pode aprovar treinos', 'content_type': content_type_plano}
    )
    # Criar a permissão customizada para remover treinos se não existir
    perm_remover, created = Permission.objects.get_or_create(
        codename='remover_treinos',
        defaults={'name': 'Pode remover treinos', 'content_type': content_type_plano}
    )
    # Criar a permissão customizada para gerar treinos se não existir
    perm_gerar, created = Permission.objects.get_or_create(
        codename='gerar_treinos',
        defaults={'name': 'Pode gerar treinos', 'content_type': content_type_plano}
    )
    # Criar a permissão customizada para cadastrar treinos se não existir
    perm_cadastrar, created = Permission.objects.get_or_create(
        codename='cadastrar_treinos',
        defaults={'name': 'Pode cadastrar treinos', 'content_type': content_type_plano}
    )
    # Criar a permissão customizada para gerenciar usuarios se não existir
    content_type_usuario = ContentType.objects.get_for_model(Usuario)
    perm_gerenciar_usuarios, created = Permission.objects.get_or_create(
        codename='gerenciar_usuarios',
        defaults={'name': 'Pode gerenciar usuários', 'content_type': content_type_usuario}
    )
    # Criar permissões CRUD para usuários
    perm_criar_usuarios, created = Permission.objects.get_or_create(
        codename='criar_usuarios',
        defaults={'name': 'Pode criar usuários', 'content_type': content_type_usuario}
    )
    perm_visualizar_usuarios, created = Permission.objects.get_or_create(
        codename='visualizar_usuarios',
        defaults={'name': 'Pode visualizar usuários', 'content_type': content_type_usuario}
    )
    perm_editar_usuarios, created = Permission.objects.get_or_create(
        codename='editar_usuarios',
        defaults={'name': 'Pode editar usuários', 'content_type': content_type_usuario}
    )
    perm_deletar_usuarios, created = Permission.objects.get_or_create(
        codename='deletar_usuarios',
        defaults={'name': 'Pode deletar usuários', 'content_type': content_type_usuario}
    )
    
    # Mostrar apenas as permissões customizadas
    permissoes = list(Permission.objects.filter(codename__in=['acessar_area_restrita', 'aprovar_treinos', 'remover_treinos', 'gerar_treinos', 'cadastrar_treinos', 'gerenciar_permissoes', 'gerenciar_usuarios', 'criar_usuarios', 'visualizar_usuarios', 'editar_usuarios', 'deletar_usuarios']))
    usuarios = Usuario.objects.all()
    usuario_selecionado = None
    permissoes_usuario = []

    translations = {
        'Can acessar area restrita': 'Pode acessar área restrita',
        'Acessar área restrita': 'Pode acessar área restrita',
        'Pode aprovar treinos': 'Pode aprovar treinos',
        'Pode remover treinos': 'Pode remover treinos',
        'Pode gerar treinos': 'Pode gerar treinos',
        'Pode cadastrar treinos': 'Pode cadastrar treinos',
        'Pode gerenciar permissões': 'Pode gerenciar permissões',
        'Pode gerenciar usuários': 'Pode gerenciar usuários',
        'Pode criar usuários': 'Pode criar usuários',
        'Pode visualizar usuários': 'Pode visualizar usuários',
        'Pode editar usuários': 'Pode editar usuários',
        'Pode deletar usuários': 'Pode deletar usuários',
    }

    for perm in permissoes:
        perm.translated_name = translations.get(perm.name, perm.name)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        if usuario_id:
            usuario_selecionado = get_object_or_404(Usuario, pk=usuario_id)
            permissoes_selecionadas = request.POST.getlist('permissoes')
            usuario_selecionado.user_permissions.set(permissoes_selecionadas)
            return redirect('gerenciar_permissoes')
        elif 'criar' in request.POST:
            form = PermissaoForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('gerenciar_permissoes')
        elif 'editar' in request.POST:
            permissao = get_object_or_404(Permission, pk=request.POST.get('permissao_id'))
            form = PermissaoForm(request.POST, instance=permissao)
            if form.is_valid():
                form.save()
                return redirect('gerenciar_permissoes')
        elif 'excluir' in request.POST:
            permissao = get_object_or_404(Permission, pk=request.POST.get('permissao_id'))
            permissao.delete()
            return redirect('gerenciar_permissoes')
    else:
        usuario_id = request.GET.get('usuario')
        if usuario_id:
            usuario_selecionado = get_object_or_404(Usuario, pk=usuario_id)
            permissoes_usuario = usuario_selecionado.user_permissions.values_list('id', flat=True)

    pode_acessar_restrita = request.user.is_authenticated and request.user.has_perm('academia.acessar_area_restrita')
    form = PermissaoForm()
    return render(request, 'permissoes/gerenciar.html', {
        'permissoes': permissoes,
        'form': form,
        'usuarios': usuarios,
        'usuario_selecionado': usuario_selecionado,
        'permissoes_usuario': permissoes_usuario,
        'pode_acessar_restrita': pode_acessar_restrita,
    })

Usuario = get_user_model()

# Opções padronizadas para o campo 'experiencia'
EXPERIENCIA_CHOICES = [
    ('iniciante', 'Iniciante'),
    ('intermediario', 'Intermediário'),
    ('avancado', 'Avançado'),
]
# Opções de objetivo disponíveis para o usuário
OBJETIVO_CHOICES = [
    ('emagrecimento', 'Emagrecimento'),
    ('resistencia', 'Resistência'),
    ('reabilitacao', 'Reabilitação'),
    ('musculacao', 'Musculação'),
]

@login_required
def home(request):
    pode_acessar_restrita = request.user.is_authenticated and request.user.has_perm('academia.acessar_area_restrita')
    return render(request, 'home.html', {'pode_acessar_restrita': pode_acessar_restrita})

@permission_required('academia.acessar_area_restrita', raise_exception=True)
def area_restrita(request):
    quantidade_usuarios = Usuario.objects.filter(perfil__tipo=2).count()  # 2 é USUARIO
    quantidade_treinos = Treino.objects.count()
    return render(request, 'restrita.html', {'quantidade_usuarios': quantidade_usuarios, 'quantidade_treinos': quantidade_treinos})

def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}), required=False, label='Senha', help_text='Deixe em branco para manter a senha atual (apenas em edição).')
    experiencia = forms.ChoiceField(choices=EXPERIENCIA_CHOICES, required=False, label='Experiência', widget=forms.Select(attrs={'class': 'form-select'}))
    objetivo = forms.ChoiceField(choices=OBJETIVO_CHOICES, required=False, label='Objetivo', widget=forms.Select(attrs={'class': 'form-select'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # No create (sem instance), senha é obrigatória
        if not self.instance.pk:
            self.fields['password'].required = True
            self.fields['password'].help_text = 'Obrigatório para novos usuários.'
        else:
            # No update, remover o campo senha para evitar alterações acidentais
            del self.fields['password']

        # Adicionar classes Bootstrap aos widgets
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['perfil'].widget.attrs.update({'class': 'form-select'})
        self.fields['peso'].widget.attrs.update({'class': 'form-control'})
        self.fields['altura'].widget.attrs.update({'class': 'form-control'})
        self.fields['sexo'].widget.attrs.update({'class': 'form-control'})
        self.fields['observacoes'].widget.attrs.update({'class': 'form-control', 'rows': 3})

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password', 'perfil', 'peso', 'altura', 'sexo', 'experiencia', 'objetivo', 'observacoes']

@login_required
@permission_required('academia.visualizar_usuarios', raise_exception=True)
def usuario_list(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuarios/list.html', {'usuarios': usuarios})

@login_required
@permission_required('academia.criar_usuarios', raise_exception=True)
def usuario_create(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            password = form.cleaned_data.get('password', '').strip()
            if password:
                usuario.set_password(password)
            usuario.save()
            return redirect('usuario_list')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/form.html', {'form': form, 'title': 'Novo Usuário'})

@login_required
@permission_required('academia.editar_usuarios', raise_exception=True)
def usuario_update(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            usuario_obj = form.save(commit=False)
            password = form.cleaned_data.get('password', '').strip()
            if password:
                usuario_obj.set_password(password)
            usuario_obj.save()
            # Se o usuário editado for o próprio logado, atualizar a sessão para evitar logout
            if request.user == usuario_obj:
                update_session_auth_hash(request, usuario_obj)
            return redirect('usuario_list')
    else:
        form = UsuarioForm(instance=usuario)
    return render(request, 'usuarios/form.html', {'form': form, 'title': 'Editar Usuário'})

@login_required
@permission_required('academia.deletar_usuarios', raise_exception=True)
def usuario_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('usuario_list')
    return render(request, 'usuarios/confirm_delete.html', {'usuario': usuario})
