# Projeto de Machine Learning - Árvore de Decisão

Este projeto implementa um modelo de árvore de decisão para classificar taxas de juros com base em dados de renda, dívidas e pontuação de crédito.

## Pré-requisitos

- Python 3.8 ou superior instalado no sistema.

## Instalação

1. **Clone ou baixe o repositório** para o seu computador.

2. **Crie um ambiente virtual (venv):**
   Abra o terminal na pasta do projeto e execute:
   ```
   python -m venv .venv
   ```

3. **Ative o ambiente virtual:**
   - No Windows (PowerShell):
     ```
     .venv\Scripts\Activate.ps1
     ```
   - No Linux/Mac:
     ```
     source .venv/bin/activate
     ```

4. **Instale as dependências:**
   ```
   pip install pandas scikit-learn matplotlib tabulate
   ```

## Como Rodar

1. Certifique-se de que os arquivos de dados estão presentes:
   - `dataset_treinamento.csv` (dados de treinamento rotulados)
   - `dataset_entrada.csv` (dados de entrada sem rótulo)

2. Execute o script principal:
   ```
   python machine_learning_decision_tree.py
   ```

   Ou, se o ambiente virtual não estiver ativado, use o caminho completo:
   ```
   .venv\Scripts\python.exe machine_learning_decision_tree.py
   ```

## Saída Esperada

O script irá:
- Treinar a árvore de decisão com os dados de treinamento.
- Aplicar o modelo aos dados de entrada.
- Exibir a acurácia, uma tabela comparativa e as regras aprendidas pela árvore.

## Resultado

Abaixo estão os resultados gerados pelo script:

### Árvore de Decisão Treinada
![Árvore de Decisão](arvore_decisao.png)

### Resultados das Previsões
![Resultados das Previsões](resultados_previsoes.png)

## Dependências

- pandas: Manipulação de dados
- scikit-learn: Modelo de árvore de decisão
- matplotlib: Visualização (opcional, para gráficos)
- tabulate: Formatação de tabelas

## Notas

- O modelo usa critério de entropia e profundidade máxima de 3 para evitar overfitting.
- A acurácia típica é em torno de 80%, dependendo dos dados.
