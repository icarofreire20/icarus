from selenium import webdriver
from time import sleep
from datetime import datetime
from datas import GetData


class ChromeAuto:
    def __init__(self):
        self.driver_path = 'chromedriver'
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('user-data-dir=Perfil')
        self.chrome = webdriver.Chrome(
            self.driver_path,
            options=self.options
        )

    def access(self, site):
        self.chrome.get(site)

    def get_html(self,url):
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
        input_login_cpf = self.chrome.find_element_by_name('identificationNumber')
        input_login_senha = self.chrome.find_element_by_name('password')
        input_login_dob = self.chrome.find_element_by_id('dob')

        input_login_cpf.send_keys(cpf)
        input_login_senha.send_keys(senha)
        input_login_dob.click()
        input_login_dob.send_keys(nascimento)

    def click_login(self):
        btn_sign_in = self.chrome.find_element_by_class_name('bt_signin')
        btn_sign_in.click()


if __name__ == '__main__':
    chrome = ChromeAuto()
    dados = GetData()
    print(datetime.now(), 'entrando no site')
    chrome.access('https://www.clear.com.br/pit/signin?controller=SignIn&referrer=http%3a%2f%2fwww.clear.com.br%2fpit')
    print(datetime.now(), 'fazendo login')
    chrome.login(cpf='xxxxxxxxxx', senha='xxxxxxxx', nascimento='ddmmaa')
    chrome.click_login()
    chrome.access('https://www.clear.com.br/pit/daytrade/Main#')
    print(datetime.now(), 'aguardando carregar completamente as informaçoes')
    sleep(15)
    print('construindo DB')
    while True:
        print(datetime.now(), 'peganado html')
        html_code = chrome.get_html('https://www.clear.com.br/pit/daytrade/Main#')
        print(datetime.now(), 'extraindo dados')
        line = dados.get_data(html_code)
        print(datetime.now(), 'salvando dados')
        dados.csv_builder(line)
        sleep(29)

        print()


    # chrome.quit()
