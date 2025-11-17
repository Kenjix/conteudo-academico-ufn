import os
import pickle
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# Caminhos para salvar os arquivos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'data', 'modelo_treino_nn.keras')
SCALER_PATH = os.path.join(BASE_DIR, 'data', 'scaler_treino_nn.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, 'data', 'encoders_treino_nn.pkl')
LABEL_PATH = os.path.join(BASE_DIR, 'data', 'labelencoder_treino_nn.pkl')

# Carregar CSV
df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'dados_treino_neural.csv'), sep=';')

# Normalização de strings
import unicodedata
def normalize_str(s):
    if not s:
        return ''
    s = str(s).strip().lower()
    s = unicodedata.normalize('NFKD', s)
    s = ''.join([c for c in s if not unicodedata.combining(c)])
    return s

def normalize_col(col):
    return col.astype(str).str.strip().str.lower().map(lambda x: unicodedata.normalize('NFKD', x)).map(lambda x: ''.join([c for c in x if not unicodedata.combining(c)]))

# Normalizar colunas categóricas
df['sexo'] = normalize_col(df['sexo'])
df['nivelexperiencia'] = normalize_col(df['nivelexperiencia'])
df['Objetivos'] = normalize_col(df['Objetivos'])
df['Plano_treino'] = normalize_col(df['Plano_treino'])

features = ['idade', 'sexo', 'peso', 'altura', 'nivelexperiencia', 'Objetivos']
target = 'Plano_treino'

X = df[features].copy()
y = df[target].copy()

# Label encoders para cada coluna categórica
encoders = {}
for col in ['sexo', 'nivelexperiencia', 'Objetivos']:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    encoders[col] = le

# Label encoder para o target
le_target = LabelEncoder()
y_enc = le_target.fit_transform(y)

# Normalização numérica
scaler = StandardScaler()
X[['idade', 'peso', 'altura']] = scaler.fit_transform(X[['idade', 'peso', 'altura']])

X_model = X.values
X_train, X_test, y_train, y_test = train_test_split(X_model, y_enc, test_size=0.2, random_state=42)

# Modelo
model = Sequential()
model.add(Dense(32, input_dim=6, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(32, activation='relu'))
model.add(Dense(len(le_target.classes_), activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=300, batch_size=8, verbose=1)

loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Acurácia do modelo (teste): {accuracy:.2%}')

# Salvar modelo e pré-processadores
model.save(MODEL_PATH)
with open(SCALER_PATH, 'wb') as f:
    pickle.dump(scaler, f)
with open(ENCODERS_PATH, 'wb') as f:
    pickle.dump(encoders, f)
with open(LABEL_PATH, 'wb') as f:
    pickle.dump(le_target, f)

print('Modelo e pré-processadores salvos com sucesso!')
with open(os.path.join(BASE_DIR, 'data', 'treino_nn.log'), 'a', encoding='utf-8') as logf:
    logf.write(f'Acurácia do modelo (teste): {accuracy:.2%}\n')
    logf.write('Modelo e pré-processadores salvos com sucesso!\n')
