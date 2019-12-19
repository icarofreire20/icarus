from bs4 import BeautifulSoup
from datetime import datetime
import csv


class GetData:

    def get_data(self, html):
        line_data = []
        time = datetime.now()
        line_data.append(time)
        soup = BeautifulSoup(html, 'html.parser')
        #  PREÇO ATUAL
        atual = soup.find('div', {'class': 'lastPrice'})
        preco_atual = atual.text
        preco_atual =preco_atual.replace(',', '.')
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

    def csv_builder(self, data):
        csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
        with open('database.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, dialect='myDialect')
            writer.writerow(data)

    '''
    def precos(self,teste):

        eco = teste
        venda1 = '546'
        venda2 = '276'
        atual = '4.75'  # necessario ser ponto por causa da separação do csv
        compra1 = '363'
        compra2 = '621'
        return eco, venda1, venda2, atual, compra1, compra2

    def csv_builder(self,url):
        valores = self.prices(url=url)

        csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)
        with open('database.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile, dialect='myDialect')
            writer.writerow(valores)

    def prices(self):
        url = 'https://www.google.com/search?q=python&oq=python&aqs=chrome..69i57j69i59j69i60l3j69i65j69i60l2.6505j0j8&sourceid=chrome&ie=UTF-8'
        response = requests.get(url)
        html = bs(response.text, 'html.parser')
        valor = html.find(id='LastPrice')
        print(valor)



with open('template1.html', 'r') as html:
    soup = BeautifulSoup(html, 'html.parser')
    atual = soup.find('div', {'class': 'lastPrice'})
    print("preco atual: ", atual.text)
    '''
