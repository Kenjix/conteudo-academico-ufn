# Academia - MVP de Recomendação de Treinos com Machine Learning

## Sobre o Projeto
Este projeto é um MVP que demonstra como Machine Learning pode apoiar instrutores de academia na criação de treinos personalizados. Utilizando Django e uma rede neural simples, o sistema analisa dados dos alunos e recomenda planos de treinos, reduzindo a variabilidade manual e melhorando o processo de decisão. O objetivo é mostrar, dentro do contexto da disciplina de Sistemas de Apoio à Decisão, como IA pode estruturar e padronizar um fluxo antes totalmente subjetivo.

## Contexto e Problema Decisório

Uma academia deseja melhorar a forma como monta planos de treino para seus alunos. Atualmente, os instrutores criam os treinos manualmente, baseados apenas em experiência pessoal. Isso gera inconsistência (sem padronização), insatisfação dos alunos e dificuldade para acompanhar o progresso.

**Problema Decisório:**  
Definir qual plano de treino (exercícios, frequência, intensidade e duração) é mais adequado para cada aluno de acordo com seus dados.

**Usuários / Decisores:**
- **Instrutor:** Principal usuário e decisor (recebe a recomendação do sistema).
- **Aluno:** Fornece dados e recebe o plano aprovado pelo instrutor.

**Dados Necessários:**
- Dados pessoais: idade, sexo, peso, altura.
- Condição física: nível de experiência.
- Treinos disponíveis de acordo com os equipamentos.
- Objetivos: emagrecimento, resistência, reabilitação, musculação, etc.


### O que é Machine Learning neste Projeto?

Machine Learning (ML) é uma técnica de IA que permite ao sistema aprender padrões a partir de dados sem ser explicitamente programado. Neste MVP:

- **Modelo Utilizado:** Rede Neural Artificial (usando TensorFlow/Keras) treinada com dados sintéticos de usuários (idade, sexo, peso, altura, experiência, objetivo).
- **Função:** O modelo prevê o tipo de treino mais adequado (ex.: "Treino A", "Treino B") baseado nas características do aluno.
- **Treinamento:** Script em `scripts/treinar_modelo_treino_nn.py` gera dados fictícios, treina o modelo e salva em `data/`.
- **Integração:** No gerador de treinos, o modelo fornece recomendações inteligentes, complementando um algoritmo heurístico simples.
- **Limitações do MVP:** Modelo básico com dados simulados; em produção, usaria dados reais para melhor acurácia.

### Funcionalidades Principais

- **Cadastro e Gerenciamento de Usuários:** CRUD completo de alunos e instrutores com permissões granulares.
- **Recomendação de Treinos:** Algoritmo heurístico e modelo de ML para sugerir treinos baseados em dados do aluno.
- **Aprovação de Planos:** Instrutores avaliam e aprovam planos antes de liberar para alunos.
- **Dashboard:** Visão geral com estatísticas e controle de permissões.
- **Sistema de Permissões:** Controle fino de acessos (aprovar, remover, gerar, cadastrar treinos, gerenciar usuários).

### Funcionalidades Principais

- **Cadastro e Gerenciamento de Usuários:** CRUD completo de alunos e instrutores com permissões granulares.
- **Recomendação de Treinos:** Algoritmo heurístico e modelo de IA (TensorFlow/Keras) para sugerir treinos baseados em dados do aluno.
- **Aprovação de Planos:** Instrutores avaliam e aprovam planos antes de liberar para alunos.
- **Dashboard:** Visão geral com estatísticas e controle de permissões.
- **Sistema de Permissões:** Controle fino de acessos (aprovar, remover, gerar, cadastrar treinos, gerenciar usuários).

### Tecnologias Utilizadas

- **Backend:** Django 5.x, Python 3.12
- **Banco de Dados:** SQLite (desenvolvimento)
- **IA/ML:** TensorFlow/Keras, scikit-learn, pandas
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Outros:** NumPy, Pickle para serialização de modelos

## Instalação

### Pré-requisitos

- Python 3.12+
- Git
- Virtualenv (opcional, mas recomendado)

### Passos

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/academia.git
   cd academia
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute as migrações:**
   ```bash
   python manage.py migrate
   ```

5. **Popule dados iniciais (treinos):**
   ```bash
   python scripts/populate_treinos.py
   ```

6. **Treine o modelo de IA (opcional, se não houver modelo pré-treinado):**
   ```bash
   python scripts/treinar_modelo_treino_nn.py
   ```

7. **Crie um superusuário:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Execute o servidor:**
   ```bash
   python manage.py runserver
   ```

Acesse em `http://127.0.0.1:8000/`.

## Uso

### Para Instrutores

1. **Login:** Use credenciais de instrutor.
2. **Gerar Treino:** Acesse "Gerador de Treinos", selecione um aluno e gere recomendações.
3. **Aprovar Planos:** Vá para "Planos Pendentes" e aprove/remova planos.
4. **Gerenciar Usuários:** Acesse "Usuários" para CRUD e "Permissões" para controle de acessos.

### Para Alunos

1. **Cadastro:** Forneça dados pessoais (idade, sexo, peso, altura, experiência, objetivo).
2. **Ver Treinos:** Acesse "Meus Treinos" para ver planos aprovados.

### Permissões

O sistema usa permissões granulares:
- `acessar_area_restrita`: Acesso à área restrita.
- `aprovar_treinos`: Aprovar planos.
- `remover_treinos`: Remover planos.
- `gerar_treinos`: Gerar recomendações.
- `cadastrar_treinos`: Cadastrar novos treinos.
- `gerenciar_permissoes`: Alterar permissões de usuários.
- `visualizar_usuarios`, `criar_usuarios`, `editar_usuarios`, `deletar_usuarios`: CRUD de usuários.

## Estrutura do Projeto

```
academia/
├── academia/          # App principal
│   ├── models/        # Modelos (Usuario, Treino, PlanoTreino, etc.)
│   ├── views/         # Views (usuario.py, treino.py)
│   └── templates/     # Templates HTML
├── core/              # Configurações do Django
├── data/              # Modelos treinados e dados
├── scripts/           # Scripts de treinamento
├── static/            # Arquivos estáticos
└── templates/         # Templates base
```