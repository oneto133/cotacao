from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from Funções import csv

class Scraping:
    def __init__(self, link="https://www.google.com/finance/quote/PETR4:BVMF"):
        self.csv = csv()
        ativos = self.csv.ler_csv(r"csv/acoes-listadas-b3.csv","Ticker")
        lista = []
        for ativo in ativos:
            lista.append(ativo)

        try:
            driver = webdriver.Chrome()

            driver.get(link)

            for Ticker in lista:
                self.main(driver, Ticker)

            driver.quit()
        except Exception as e:
            print("Erro inesperado ", e)
        
    def main(self, driver, Ticker):

        try:
            barra_de_busca = driver.find_element(By.CLASS_NAME, "Ax4B8.ZAGvjd")

            sleep(2)
            barra_de_busca.click()

            barra_de_busca.clear()

            barra_de_busca.send_keys(Ticker)

            botão_de_pesquisa = driver.find_element(By.CLASS_NAME, "gb_De")
            botão_de_pesquisa.click()

            sleep(2)
            url = driver.current_url
            self.csv.escrever_csv(conteudo=(Ticker,url,"bdr","2"), nome=r"csv/url.csv", tipo="a")


        except Exception as e:
            print(e)
        

if __name__ == "__main__":
    Scraping()