import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import pickle

class AnalizeDados:

    @staticmethod
    def inset_result(db, mins, delta):
        '''
        Summary: pega o data base com as informações que foram coletadas durante o pregão e insere as classes
            a serem previstas para que a inteligencia artificial possa aprender
        :param db: (str) caminho do database a ser analizado, .csv
        :param mins: (int) número de minutos a ser calculado a difernça de preço
        :param delta: (int) diferença numerica do preço, objetivo de ganho da operação
        :return: salva uma nova base de dados com as classes de resultado para a AI poder aprender
        '''
        #  um registro por minuto
        df = pd.read_csv(db)
        result_classifier = []
        result_regression = []
        #  calcula a variaçao do preço e tambem o preço futuro
        for i in range(len(df) - mins):
            valor = float(df.iloc[i + mins, 1]) - float(df.iloc[i, 1])
            result_regression.append(float(df.iloc[i + mins, 1]))
            if valor >= delta:
                result_classifier.append('comprar')
            elif valor <= -delta:
                result_classifier.append('vender')
            else:
                result_classifier.append('permanecer')

        #  remove os últimos registros que não receberam um valor calculado pela função
        df = df.iloc[:-mins, :]

        df['result_classifier'] = result_classifier
        df['result_regression'] = result_regression
        db = db.replace('.csv', '')
        data_base = str(f'dataset/{db}_{mins}min_{delta}delta.csv')
        df.to_csv(data_base, index=0, mode='w', header=False)


    @staticmethod
    def predicts(db, method='RandomForest'):
        deltat = datetime.now()
        df = pd.read_csv(db)
        previsores = df.iloc[:, 1:25].values
        classe = df.iloc[:, 25].values

        scaler = StandardScaler()
        scaler.fit(previsores)
        previsores = scaler.transform(previsores)

        previsores_treinamento, previsores_teste, classe_treinamento, classe_teste = train_test_split(previsores,
                                                                                classe, test_size=0.1, random_state=0)

        classificador = []
        if method == 'NB':
            classificador = GaussianNB()
        elif method == 'tree':
            classificador = DecisionTreeClassifier(criterion='entropy')
        elif method == 'RandomForest':
            classificador = RandomForestClassifier(n_estimators=200, criterion='entropy', random_state=0, warm_start=True)
        elif method == 'kNN':
            classificador = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        elif method == 'SVM':
            classificador = SVC(kernel='rbf', random_state=0)  # kernel types: rbf, linear, sigmoid
        elif method == 'neural_network':
            classificador = MLPClassifier(verbose=False,
                                          max_iter=20000,
                                          tol=0.0000005,
                                          solver='adam',
                                          hidden_layer_sizes=(100, 100),
                                          activation='identity')
        else: print('Selecione metodo Valido')

        classificador.fit(previsores_treinamento, classe_treinamento)

        previsoes = classificador.predict(previsores_teste)

        precisao = accuracy_score(classe_teste, previsoes)
        if precisao > 0.9689922480620154:
            print('precisão melhorada: ', precisao)
            with open("stocks1.pickle", "wb") as f:
                pickle.dump(classificador, f)

        if __name__ == '__main__':
            matriz = confusion_matrix(classe_teste, previsoes)
            print(f'{method}:{precisao*100:.5}%')
            print('tempo de execuçao do metodo: ', datetime.now() - deltat)
            print(classificador.classes_)
            print(matriz)
            print(len(previsoes))

        return scaler


if __name__ == '__main__':
    dados = AnalizeDados()

    #  dados.inset_result(db='database.csv', mins=15, delta=5)

    banco_dados = 'dataset/database_15min_5delta.csv'
    dados.predicts(banco_dados, method='RandomForest')

