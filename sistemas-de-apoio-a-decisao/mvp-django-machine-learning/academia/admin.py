from django.contrib import admin
from .models.exercicio import Exercicio
from .models.equipamento import Equipamento
from .models.treino import Treino, TreinoExercicio, PlanoTreino


@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
	list_display = ('descricao',)


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
	list_display = ('descricao', 'equipamento')


class TreinoExercicioInline(admin.TabularInline):
	model = TreinoExercicio
	extra = 1


@admin.register(Treino)
class TreinoAdmin(admin.ModelAdmin):
	list_display = ('nome', 'objetivo', 'nivel_experiencia')
	inlines = (TreinoExercicioInline,)


@admin.register(PlanoTreino)
class PlanoTreinoAdmin(admin.ModelAdmin):
	list_display = ('treino', 'usuario', 'objetivo', 'frequencia_semanal', 'aprovado')
