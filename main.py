from bs4 import BeautifulSoup
import requests
from Funções import Tratamento_de_strings

class conexão:
    def __init__(self, url="https://www.google.com/finance/quote/PETR4:BVMF"):
        try:
            self.resposta = requests.get(url)
            tratamento = Tratamento_de_strings()
            if self.resposta.status_code == 200:
                soup = BeautifulSoup(self.resposta.text, "html.parser")
                self.cotação = soup.select_one("div.YMlKec.fxKbKc")
                self.código = url[37:42]
                self.variações = soup.select("div.P6K39c")
                self.rendimentos = self.variações[6]
                print("cotação atual ", tratamento.tratar_dados_de_url(self.cotação), 
                    "Código", self.código,
                    "variações do dia", tratamento.tratar_dados_de_url(self.variações[2]),
                    "rendimento atual", tratamento.tratar_dados_de_url(self.rendimentos), 
                    f"isso equivale a R${tratamento.tratar_valores_url(self.cotação, self.rendimentos):.2f} ao ano.")
        except Exception as e:
            print("Erro inesperado: ", e)
        except:
            print("Erro, url inválida!")
if __name__ == "__main__":
    conexão()
