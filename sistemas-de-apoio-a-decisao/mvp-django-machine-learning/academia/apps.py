import os
from django.apps import AppConfig

class AcademiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academia'

    def ready(self):
        # Executa o script de treinamento do modelo se o arquivo não existir
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'data', 'modelo_treino_nn.keras')
        if not os.path.exists(model_path):
            import subprocess
            script_path = os.path.join(base_dir, 'scripts', 'treinar_modelo_treino_nn.py')
            if os.path.exists(script_path):
                print('Treinando modelo NN automaticamente...')
                subprocess.run(['python', script_path], check=True)
            else:
                print('Script de treinamento não encontrado:', script_path)
from django.apps import AppConfig


class AcademiaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'academia'
