import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier


class AnalizeDados:

    @staticmethod
    def inset_result(db, mins, delta):
        mins *= 2
        df = pd.read_csv(db)
        result = []
        for i in range(len(df) - mins):
            #  result.append(df.iloc[i, 0] - df.iloc[i + 2, 0])
            valor = float(df.iloc[i + mins, 1]) - float(df.iloc[i, 1])
            #  valor = float(valor)
            if valor >= delta:
                result.append('comprar')
            elif valor <= -delta:
                result.append('vender')
            else:
                result.append('permanecer')

        for i in range(mins):
            result.append('permanecer')

        df['result'] = result
        mins = int(mins / 2)
        db = db.replace('.csv', '')
        data_base = str(f'dataset/{db}_{mins}min_{delta}delta.csv')
        df.to_csv(data_base, index=0, mode='a', header=False)

    @staticmethod
    def predicts(db, method):
        df = pd.read_csv(db)
        previsores = df.iloc[:, 1:20].values
        classe = df.iloc[:, 20].values

        scaler = StandardScaler()  # uso nao altera o resultado
        previsores = scaler.fit_transform(previsores)

        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores,
                                                                                classe, test_size=0.2, random_state=0)

        if method == 'NB':
            classificador = GaussianNB()  #  0.66 accuracy
        elif method == 'tree':
            classificador = DecisionTreeClassifier(criterion='entropy')  # 0.83 accuracy
        classificador.fit(previsores_treinamento, classe_treinamento)
        previsoes = classificador.predict(previsores_teste)

        precisao = accuracy_score(classe_teste, previsoes)
        matriz = confusion_matrix(classe_teste, previsoes)
        print(classificador.predict([[4053.0,201,445,547,675,667,642,924,562,1016,253,439,1284,961,830,976,643,961,804]]))
        print(f'{method}:{precisao}%')
        print(classificador.classes_)
        print(matriz)


dados = AnalizeDados
#  dados.inset_result(db='database_dollar.csv', mins=1, delta=1)
dados.predicts('dataset/database_indice_5min_50delta.csv', method='NB')
dados.predicts('dataset/database_indice_5min_50delta.csv', method='tree')

'''
df = pd.read_csv('database.csv', index_col=0)  # LER SEM O INDEX
df.to_csv('database.csv', index=0)  #  SALVAR DF SEM COLUNA INDEX
'''
