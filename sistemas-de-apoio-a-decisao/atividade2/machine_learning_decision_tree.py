# Importa a biblioteca pandas para manipulação de dados em DataFrames
import pandas as pd  # pandas permite ler CSV, filtrar colunas e criar novas colunas

# Importa a árvore de decisão do scikit-learn para classificação
from sklearn.tree import DecisionTreeClassifier  # modelo supervisionado

# Importa funções de visualização de árvore e relatório textual
from sklearn.tree import plot_tree, export_text  # utilitário para visualizar e extrair regras em texto

# Importa matplotlib para exibir o gráfico da árvore (opcional)
import matplotlib.pyplot as plt  # biblioteca de plots 2D

# Importa lib tabulate para exibir accuracia tabulada
from tabulate import tabulate

# ---------------------------
# 1) CARREGAR O DATASET DE TREINO (ROTULADO)
# ---------------------------

# Lê o CSV de treino com separador ';' e vírgula como separador decimal
treino = pd.read_csv("./assets/datasets/dataset_treinamento.csv", sep=";", decimal=",")  # contém 'renda', 'dividas', 'pontuacao_credito', 'taxa_juros'

# Separa as features (X) e o alvo (y) a partir do DataFrame de treino
X_train = treino[["renda", "dividas", "pontuacao_credito"]]   # três colunas numéricas usadas como entradas do modelo
y_train = treino["taxa_juros"].str.replace("%", "").astype(int) # coluna de saída (classe), calculada pela regra oficial (política) com conversão "3%" -> 3, "5%" -> 5, etc.

# ---------------------------
# 2) TREINAR A ÁRVORE DE DECISÃO
# ---------------------------

# Cria o classificador de árvore de decisão, definindo critério, profundidade e semente para reprodutibilidade
clf = DecisionTreeClassifier(criterion="entropy", max_depth=3, random_state=42)  # limita complexidade e fixa random_state

# Ajusta (treina) o modelo com os dados de treino
clf.fit(X_train, y_train)  # o modelo aprende a separar as classes seguindo divisões que maximizam informação

# ---------------------------
# 3) CARREGAR O DATASET DE ENTRADA (50 LINHAS, SEM RÓTULO)
# ---------------------------

# Lê o CSV de entrada com as mesmas configurações de separador e decimal
entrada = pd.read_csv("./assets/datasets/dataset_entrada.csv", sep=";", decimal=",")  # contém 'renda', 'dividas' e 'pontuacao_credito' apenas

# ---------------------------
# 4) DEFINIR A REGRA OFICIAL (VERDADE-TERRENO) E ROTULAR A ENTRADA
# ---------------------------

# Função que aplica a política oficial do banco para taxa de juros
def regra_taxa(renda, dividas, pontuacao_credito):
    if pontuacao_credito >= 80 and dividas < 2 and renda >= 5:
        return 3   # juros muito baixos para clientes excelentes
    if pontuacao_credito >= 60 and dividas < 5:
        return 5   # juros baixos
    if pontuacao_credito >= 40:
        return 7   # juros médios
    return 10       # caso contrário, juros altos

# Cria a coluna 'taxa_verdade' aplicando a regra oficial linha a linha na entrada
entrada["taxa_verdade"] = [
    regra_taxa(r, d, s) for r, d, s in zip(
        entrada["renda"], entrada["dividas"], entrada["pontuacao_credito"]
    )
]

# ---------------------------
# 5) REALIZAR A PREDIÇÃO DO MODELO E COMPARAR
# ---------------------------

# Predição da árvore
entrada["taxa_prevista"] = clf.predict(entrada[["renda", "dividas", "pontuacao_credito"]])

# Compara previsão vs. verdade
entrada["resultado"] = [
    "ACERTOU" if p == v else "ERROU"
    for p, v in zip(entrada["taxa_prevista"], entrada["taxa_verdade"])
]

# Calcula acurácia
acuracia = (entrada["taxa_prevista"] == entrada["taxa_verdade"]).mean()

# ---------------------------
# 6) IMPRIMIR AS 50 LINHAS COM O MARCADOR DE ACERTO/ERRO
# ---------------------------

colunas_exibir = ["renda", "dividas", "pontuacao_credito", "taxa_verdade", "taxa_prevista", "resultado"]

# Cria uma cópia para exibição com valores renda e dividas multiplicados por 1k para exibição
saida_fmt = entrada[colunas_exibir].copy()
saida_fmt["renda"] = (saida_fmt["renda"] * 1000).map("R${:,.0f}".format)
saida_fmt["dividas"] = (saida_fmt["dividas"] * 1000).map("R${:,.0f}".format)

# Exibe acurácia
print(f"Acurácia no conjunto de entrada (50 linhas): {acuracia:.3f}\n")

# Exibe tabela formatada com tabulate
print(tabulate(saida_fmt.values, headers=saida_fmt.columns, tablefmt="github", stralign="left"))

# ---------------------------
# 7) VISUALIZAR A ÁRVORE E AS REGRAS TEXUAIS PARA SLIDES
# ---------------------------

# Cria uma figura para o gráfico da árvore de decisão
plt.figure(figsize=(10, 6))  # define tamanho da figura para facilitar leitura

# Desenha a árvore com nomes das features e classes, incluindo caixas coloridas
plot_tree(
    clf,  # modelo treinado
    feature_names=["renda", "dividas", "pontuacao_credito"],  # nomes das entradas
    class_names=[f"{c}%" for c in clf.classes_],  # rótulos de classe com símbolo de porcentagem
    filled=True,  # preenche os nós com cor indicando pureza
    rounded=True,  # deixa as caixas com cantos arredondados
    precision=2    # número de casas exibidas nas condições
)  # finaliza chamada do plot_tree

# Adiciona um título ao gráfico
plt.title("Árvore de Decisão - Cálculo da Taxa de Juros (Treinada no conjunto de 1000 linhas)", fontsize=14) # título do gráfico

# Salva o gráfico como imagem
plt.savefig('./assets/image/arvore_decisao.png', dpi=300, bbox_inches='tight')  # salva em alta resolução

# Ajusta layout para não cortar textos
plt.tight_layout()  # melhora o espaçamento automaticamente

# Exibe o gráfico na tela
plt.show()  # mostra a figura renderizada

# Gera uma representação textual das regras aprendidas
print("\nRegras aproximadas aprendidas pela árvore:\n")  # texto introdutório
print(export_text(clf, feature_names=["renda", "dividas", "pontuacao_credito"]))  # imprime as regras em formato de árvore textual