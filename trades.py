from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
from datas import GetData
import threading
from AI import AnalizeDados


class ChromeAuto:
    def __init__(self):
        """
        Summary:
            set up das configuraçoes do webdriver
        """
        self.driver_path = 'chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def access(self, site):
        """
        Summary:
            acessa o site
        :param site: (str) insira url do site a ter o codigo html copiado
        :return:
            carrega a url passada no parametro
        """
        self.chrome.get(site)

    def get_html(self, url):
        """
        Summary:
            pega o codigo html da pagina

        :param url: (str) insira url do site a ter o codigo html copiado

        :return:
            codigo html da pagina
        """
        self.chrome.get(url)
        html = self.chrome.page_source
        '''html = str(html)
        Html_file = open("template1.html", "w")
        Html_file.write(html)
        Html_file.close()'''
        return html

    def quit(self):
        self.chrome.quit()

    def login(self, cpf, senha, nascimento):
        """
        Summary:
            localiza campos na pagina e os preenche com cpf, senha e data de nascimento

        :param cpf: (int) insira cpf sem pontos ou traço
        :param senha: (int) senha é estipulada pelo site sendo 6 digitos apenas
        :param nascimento: (int) insira data de nascimento sem traços ou barras, apenas numeros

        :return:
            formulario de login preenchido e clica no botão de login
        """
        input_login_cpf = self.chrome.find_element_by_name('identificationNumber')
        input_login_senha = self.chrome.find_element_by_name('password')
        input_login_dob = self.chrome.find_element_by_id('dob')

        input_login_cpf.send_keys(cpf)
        input_login_senha.send_keys(senha)
        input_login_dob.click()
        input_login_dob.send_keys(nascimento)

        btn_sign_in = self.chrome.find_element_by_class_name('bt_signin')
        btn_sign_in.click()


def get_input():
    """
    Summary
        Função que roda em paralelo com  a função principal do trader
        Observa o teclado, caso o usuario digite "s" ou "S"
        a função get_input interrompe o andamento do script principal
    :return:
        bool: Flag
    """
    global flag
    while flag:
        keystrk = input('Pressione "s" para sair\n')
        keystrk = keystrk.lower()
        # thread doesn't continue until key is pressed
        if keystrk == 's':
            flag = False
            print('Fechando o TRADER...')


flag = True
if __name__ == '__main__':
    i = threading.Thread(target=get_input)
    i.start()
    chrome = ChromeAuto()
    dados = GetData()

    chrome.access('https://www.clear.com.br/pit/signin?controller=SignIn&referrer=http%3a%2f%2fwww.clear.com.br%2fpit')
    chrome.login(cpf='xxxxxxxxxxx', senha='xxxxxx', nascimento='ddmmaa')
    chrome.access('https://www.clear.com.br/pit/daytrade/Main#')
    sleep(15)  # aguarda o carregamento total da pagina
    print('contruindo DB')
    while flag:
        #  sincroniza com o relogio para que o script rode a cada minuto
        minute = float(str(datetime.now())[17:])
        sleep(60 - minute)
        dt = datetime.now() + timedelta(seconds=58)
        max_min = [0, 0]
        print(datetime.now(), 'monitorando...')
        while datetime.now() < dt and flag:
            #  monitora o preço maximo e minimo (aprox 115 interaçoes por minuto)
            html_code = chrome.get_html('https://www.clear.com.br/pit/daytrade/Main#')
            max_min = dados.get_min_max(html_code)
        html_code = chrome.get_html('https://www.clear.com.br/pit/daytrade/Main#')
        print(datetime.now(), 'extraindo dados')
        line = dados.get_data(html_code)
        print(datetime.now(), 'salvando dados')
        line = dados.add_info(line, max_min)
        dados.csv_builder(line)

    chrome.quit()
