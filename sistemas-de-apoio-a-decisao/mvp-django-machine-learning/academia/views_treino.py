
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .models.treino import Treino, PlanoTreino, Objetivo
from .models.exercicio import Exercicio
from django.contrib.auth import get_user_model
import os

Usuario = get_user_model()

@login_required
@permission_required('academia.cadastrar_treinos', raise_exception=True)
def cadastrar_treino(request):
    sucesso = False
    if request.method == 'POST':
        nome = request.POST.get('nome')
        objetivo = request.POST.get('objetivo')
        nivel_experiencia = request.POST.get('nivel_experiencia')
        descricao = request.POST.get('descricao')
        if nome and objetivo:
            Treino.objects.create(
                nome=nome,
                objetivo=objetivo,
                nivel_experiencia=nivel_experiencia,
                descricao=descricao
            )
            sucesso = True
    return render(request, 'treinos/cadastrar_treino.html', {
        'objetivos': Objetivo.choices,
        'sucesso': sucesso
    })


@login_required
@permission_required('academia.acessar_area_restrita', raise_exception=True)
def treinos_list(request):
    treinos = Treino.objects.all()
    return render(request, 'treinos/list.html', {'treinos': treinos})


@login_required
@permission_required('academia.acessar_area_restrita', raise_exception=True)
def treinos_detail(request, pk):
    treino = get_object_or_404(Treino, pk=pk)
    return render(request, 'treinos/detail.html', {'treino': treino})


def recomendar_treino_para_usuario(usuario, objetivo=None, equipamentos_ids=None):
    # Recomendador simples heurístico:
    # 1) Preferir treinos que batam com o objetivo pedido (se informado)
    # 2) Filtrar por nivel_experiencia baseado em usuario.experiencia
    # 3) Se equipamentos_ids fornecidos, preferir treinos cujo exercicios usem esses equipamentos
    candidatos = Treino.objects.all()

    # Filtrar por objetivo se informado
    if objetivo:
        candidatos = candidatos.filter(objetivo__iexact=objetivo)

    experiencia = (usuario.experiencia or '').lower()
    if experiencia:
        candidatos = candidatos.filter(nivel_experiencia__icontains=experiencia)

    # Se equipamentos_ids informados, tentar reduzir candidatos
    if equipamentos_ids:
        candidatos = candidatos.filter(exercicios__equipamentos__id__in=equipamentos_ids).distinct()

    # Calcular IMC simples e preferir treinos por objetivo se nenhuma preferência foi passada
    try:
        imc = None
        if usuario.peso and usuario.altura:
            imc = float(usuario.peso) / ((float(usuario.altura) / 100.0) ** 2)
    except Exception:
        imc = None

    # Se ainda não restarem candidatos, relaxar filtros
    if not candidatos.exists():
        candidatos = Treino.objects.all()
        if experiencia:
            candidatos = candidatos.filter(nivel_experiencia__icontains=experiencia)

    # Ordenar por correspondência simples: objetivo first, then nivel_experiencia
    def score(t):
        s = 0
        if objetivo and t.objetivo.lower() == objetivo.lower():
            s += 10
        if experiencia and t.nivel_experiencia and experiencia in t.nivel_experiencia.lower():
            s += 5
        return s

    candidatos_list = list(candidatos.distinct())
    candidatos_list.sort(key=score, reverse=True)

    # Retornar até 10 recomendações
    return candidatos_list[:10]


@login_required
def treinos_sugerir(request, usuario_id=None):
    # Usuários podem ver recomendações para si; instrutores podem ver para alunos
    if usuario_id:
        usuario = get_object_or_404(Usuario, pk=usuario_id)
    else:
        usuario = request.user

    objetivo = request.GET.get('objetivo')
    equipamentos = request.GET.getlist('equipamento')
    equipamentos_ids = [int(e) for e in equipamentos if e.isdigit()]

    recomendados = recomendar_treino_para_usuario(usuario, objetivo=objetivo, equipamentos_ids=equipamentos_ids)
    return render(request, 'treinos/sugerir.html', {
        'usuario': usuario,
        'recomendados': recomendados,
        'objetivos': Objetivo.choices,
        'selecionado_objetivo': objetivo,
    })


@login_required
@permission_required('academia.gerar_treinos', raise_exception=True)
def treinos_gerador(request):
    import os
    usuarios = Usuario.objects.filter(perfil__tipo=2)
    selected = None
    result = None

    if request.method == 'GET':
        user_id = request.GET.get('usuario')
        if user_id and user_id.isdigit():
            selected = get_object_or_404(Usuario, pk=int(user_id))
        return render(request, 'treinos/generator.html', {'usuarios': usuarios, 'selected': selected})

    # POST: gerar treino
    if request.method == 'POST':
        user_id = request.POST.get('usuario')
        if not user_id:
            return redirect('treinos_gerador')
        usuario = get_object_or_404(Usuario, pk=int(user_id))


        import unicodedata
        def normalize_str(s):
            if not s:
                return ''
            s = s.strip().lower()
            s = unicodedata.normalize('NFKD', s)
            s = ''.join([c for c in s if not unicodedata.combining(c)])
            return s

        # Extrair features do usuário para o novo CSV
        idade = int(getattr(usuario, 'idade', 30)) if hasattr(usuario, 'idade') and usuario.idade else 30
        sexo = normalize_str(usuario.sexo or '')
        peso = float(usuario.peso) if usuario.peso else 70.0
        altura = float(usuario.altura) if usuario.altura else 170.0
        experiencia = normalize_str(usuario.experiencia or '')
        objetivo = normalize_str(getattr(usuario, 'objetivo', '') or '')


        def get_last_accuracy():
            log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'treino_nn.log')
            if not os.path.exists(log_path):
                return None
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in reversed(lines):
                if 'Acurácia do modelo' in line:
                    return line.strip().split(':')[-1].strip()
            return None

        try:
            import numpy as np
            import pickle
            import unicodedata
            from tensorflow.keras.models import load_model
            import logging
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            MODEL_PATH = os.path.join(BASE_DIR, 'data', 'modelo_treino_nn.keras')
            SCALER_PATH = os.path.join(BASE_DIR, 'data', 'scaler_treino_nn.pkl')
            ENCODERS_PATH = os.path.join(BASE_DIR, 'data', 'encoders_treino_nn.pkl')
            LABEL_PATH = os.path.join(BASE_DIR, 'data', 'labelencoder_treino_nn.pkl')

            # Carregar modelo e pré-processadores
            model = load_model(MODEL_PATH)
            with open(SCALER_PATH, 'rb') as f:
                scaler = pickle.load(f)
            with open(ENCODERS_PATH, 'rb') as f:
                encoders = pickle.load(f)
            with open(LABEL_PATH, 'rb') as f:
                le_target = pickle.load(f)

            # Normalizar valores do usuário
            idade_val, peso_val, altura_val = scaler.transform([[idade, peso, altura]])[0]
            sexo_val = encoders['sexo'].transform([sexo])[0] if sexo in encoders['sexo'].classes_ else 0
            experiencia_val = encoders['nivelexperiencia'].transform([experiencia])[0] if experiencia in encoders['nivelexperiencia'].classes_ else 0
            objetivo_val = encoders['Objetivos'].transform([objetivo])[0] if objetivo in encoders['Objetivos'].classes_ else 0

            user_vec = np.array([[idade_val, sexo_val, peso_val, altura_val, experiencia_val, objetivo_val]])
            pred = model.predict(user_vec)
            pred_idx = int(np.argmax(pred))
            plano_predito = le_target.inverse_transform([pred_idx])[0]
            usado_nn = True
            accuracy = get_last_accuracy()
            # Se a acurácia estiver entre 0 e 1, converter para porcentagem
            try:
                if accuracy is not None:
                    acc_float = float(accuracy.replace(',', '.'))
                    if acc_float <= 1.0:
                        accuracy = acc_float * 100
                    else:
                        accuracy = acc_float
            except Exception:
                pass
            print(f"Accuracy: {accuracy}, type: {type(accuracy)}")

            # LOGS DEBUG
            print('--- LOG RECOMENDACAO NN ---')
            print('Possiveis classes do modelo:', list(le_target.classes_))
            print('Treinos cadastrados:', list(Treino.objects.values_list('nome', flat=True)))

        except Exception as e:
            plano_predito = None
            usado_nn = False
            accuracy = None
            print('Erro no modelo NN:', e)

        treino_sugerido = None
        if plano_predito:
            # Busca tolerante a maiúsculas/minúsculas e espaços extras
            prefixes = [
                f'Treino {plano_predito.upper()}',
                f'Treino {plano_predito.lower()}',
                f'Treino {plano_predito.strip().capitalize()}'
            ]
            for prefix in prefixes:
                treino_sugerido = Treino.objects.filter(nome__istartswith=prefix).first()
                if treino_sugerido:
                    break
            if not treino_sugerido:
                print('Nenhum treino encontrado para o plano predito:', plano_predito)

        if treino_sugerido:
            plano = {
                'usuario': usuario,
                'treino': treino_sugerido,
                'frequencia_semanal': 3,
                'duracao_semanas': 8,
            }
            result = {'tipo': 'modelo', 'plano': plano, 'usou_nn': usado_nn, 'score': None, 'accuracy': accuracy, 'plano_predito': plano_predito}
        else:
            descricao = 'Treino sugerido: 3 sessões/semana — foco em resistência e mobilidade.'
            result = {'tipo': 'texto', 'descricao': descricao, 'usou_nn': usado_nn, 'score': None, 'accuracy': accuracy, 'plano_predito': plano_predito}

        return render(request, 'treinos/generated.html', {'result': result, 'usuario': usuario})


@login_required
@permission_required('academia.gerar_treinos', raise_exception=True)
def treinos_salvar(request):
    # Salva um PlanoTreino no banco a partir do resultado gerado
    if request.method != 'POST':
        return redirect('treinos_gerador')

    usuario_id = request.POST.get('usuario_id')
    treino_id = request.POST.get('treino_id')
    frequencia = request.POST.get('frequencia', 3)
    duracao = request.POST.get('duracao', 8)

    if not usuario_id or not treino_id:
        messages.error(request, 'Dados incompletos para salvar o plano.')
        return redirect('treinos_gerador')

    usuario = get_object_or_404(Usuario, pk=int(usuario_id))
    treino = get_object_or_404(Treino, pk=int(treino_id))

    plano = PlanoTreino.objects.create(
        usuario=usuario,
        treino=treino,
        objetivo=treino.objetivo,
        frequencia_semanal=int(frequencia),
        duracao_semanas=int(duracao),
        criado_por=request.user,
        aprovado=False,
    )
    messages.success(request, f'Plano salvo para {usuario.username}.')
    return redirect('treinos_detail', pk=treino.pk)


@login_required
@permission_required('academia.acessar_area_restrita', raise_exception=True)
def planos_pendentes(request):
    planos = PlanoTreino.objects.filter(aprovado=False).select_related('usuario', 'treino').order_by('criado_em')
    return render(request, 'treinos/pendentes.html', {'planos': planos})


@login_required
@permission_required('academia.remover_treinos', raise_exception=True)
def plano_remover(request, pk):
    plano = get_object_or_404(PlanoTreino, pk=pk)
    if request.method == 'POST':
        plano.delete()
        messages.success(request, f'Plano para {plano.usuario.username} removido.')
        return redirect('meus_treinos')
    return render(request, 'treinos/plano_confirm_delete.html', {'plano': plano})


@login_required
@permission_required('academia.aprovar_treinos', raise_exception=True)
def plano_aprovar(request, pk):
    plano = get_object_or_404(PlanoTreino, pk=pk)
    if request.method == 'POST':
        plano.aprovado = True
        plano.save()
        messages.success(request, f'Plano para {plano.usuario.username} aprovado.')
        return redirect('planos_pendentes')
    return render(request, 'treinos/plano_confirm_approve.html', {'plano': plano})
