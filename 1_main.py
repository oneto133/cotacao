from bs4 import BeautifulSoup
import requests

class conexão:
    def __init__(self, url="https://www.google.com/finance/quote/PETR4:BVMF"):
        self.resposta = requests.get(url)
        if self.resposta.status_code == 200:
            soup = BeautifulSoup(self.resposta.text, "html.parser")
            self.cotação = soup.select_one("div.YMlKec.fxKbKc")
            self.código = url[37:42]
            self.variações = soup.select("div.P6K39c")
            self.rendimentos = self.variações[6]
            print("cotação atual ", self.tratar(self.cotação), 
                 "Código", self.código,
                 "variações do dia", self.tratar(self.variações[2]),
                 "rendimento atual", self.tratar(self.rendimentos), 
                 f"isso equivale a R${self.valores(self.cotação, self.rendimentos):.2f} ao ano.")

    def tratar(self, texto_a_tratar):
        texto = str(texto_a_tratar.text.split())
        texto_sem_aspas = texto.replace("'", "").replace(",", "")
        texto_tratado = texto_sem_aspas[1:-1]
        return texto_tratado
    
    def valores(self, valor, porcentagem):
        preço = float(self.tratar(valor)[2:])
        divisor = float(self.tratar(porcentagem)[:-1])
        print(preço, divisor)
        resultado = preço * (divisor / 100)
        return resultado


if __name__ == "__main__":
    conexão()



#sdsdksdsdjsdsjdskdjsd
#sdskdsdjsjdsdksdjs