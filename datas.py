from bs4 import BeautifulSoup
from datetime import datetime
import csv
import pandas as pd


class GetData:

    @staticmethod
    def get_data(html):
        """
        Summary:
            analiza o codigo html para extrair dados sobre preço atual e volume dos compradores e vendedores

        :param html: codigo html

        :return:
            (list) lista com valores extraidos do site
        """
        line_data = []
        time = str(datetime.now())
        line_data.append(time)
        soup = BeautifulSoup(html, 'html.parser')
        #  PREÇO ATUAL
        atual = soup.find('div', {'class': 'lastPrice'})
        preco_atual = atual.text
        preco_atual = preco_atual.replace(',', '.')
        line_data.append(preco_atual)
        #  VOLUME COMPRADORES
        buyers = soup.findAll("div", {"class": "offers offersBuy"})
        index = 0
        for buyer in buyers:
            volumes = buyer.findAll("div", {"class": "offerMeioQtd"})
            for volume in volumes:
                if index < 9:
                    volume = volume.text
                    volume = volume.replace('.', '')
                    line_data.append(volume)
                    index += 1
                else:
                    break
        #  VOLUME VENDEDORES
        sellers = soup.findAll("div", {"class": "offers offersSell"})
        index = 0
        for seller in sellers:
            volumes = seller.findAll("div", {"class": "offerMeioQtd"})
            for volume in volumes:
                if index < 9:
                    volume = volume.text
                    volume = volume.replace('.', '')
                    line_data.append(volume)
                    index += 1
                else:
                    break
        return line_data

    @staticmethod
    def get_min_max(html):
        """
        Summary:
            observa os valores, fazendo aproximadamente 115 interaçoes por minuto para armazenar os valores de
            preço maximo e minimo
        :param html: codigo html extrair os dados que interessa para as previsoes da AI
        :return:
            (list) lista com valores de preço maximo e minimo
        """
        xtreme_vals = []
        preco_max = 0
        preco_min = 0
        soup = BeautifulSoup(html, 'html.parser')
        #  PREÇO ATUAL
        atual = soup.find('div', {'class': 'lastPrice'})
        preco_atual = atual.text
        preco_atual = preco_atual.replace(',', '.')
        preco_atual = float(preco_atual)
        if preco_atual > preco_max:
            preco_max = preco_atual
        elif preco_atual < preco_min:
            preco_min = preco_atual
        xtreme_vals.append(preco_max)
        xtreme_vals.append(preco_min)
        return xtreme_vals

    @staticmethod
    def add_info(data, xtreme_vals):
        """
        Summary:
            processa os dados e adiciona as medias moveis exponenciais de 13 e 72 periodos
            adiciona tambem a hora (int) em que foi coletado o dado, será usado como parametro pela AI

        :param xtreme_vals: (list) valores de preço maximo e minimo dentro do minuto monitorado
        :param data: (list) lista que retorna de get data adicionada com os valoeres de preço minimo e maximo

        :return:
            (list) lista com todos os valores para serem salvos

        """
        data.append(xtreme_vals[0])
        data.append(xtreme_vals[1])
        df = pd.read_csv('database.csv')
        mme = df.iloc[len(df) - 1:, 22:24].values
        preco = data[1]
        preco = float(preco)
        mme13 = float(mme[0][0])
        mme72 = float(mme[0][1])
        new_mme13 = round((preco - mme13) * 0.143 + mme13, 2)
        new_mme72 = round((preco - mme72) * 0.03 + mme72, 2)
        hora = data[0][11:13]
        data.append(new_mme13)
        data.append(new_mme72)
        data.append(hora)
        print(data)
        return data

    @staticmethod
    def csv_builder(data):
        """
        Summary:
            adiciona dados coletados e tratados ao database

        :param data: (list) lista com dados do tempo monitorado

        :return:
            line in 'database.csv'
        """
        csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
        with open('database.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, dialect='myDialect')
            writer.writerow(data)
