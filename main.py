from bs4 import BeautifulSoup
import requests
from Funções import Tratamento_de_strings, csv, Horarios, moeda

class conexão:

    def __init__(self):

        lista_de_url = []
        lista_de_ticker = []
        arquivo = csv()
        ler = arquivo.ler_csv(r"csv/url.csv", "url")
        Ticker = arquivo.ler_csv(r"csv/url.csv", "codigo")
        

        for url in ler:
            lista_de_url.append(url)
        
        for ticker in Ticker:
            lista_de_ticker.append(ticker)
        
        cont = 0
        for c in range(0,len(lista_de_url)):
            tipo = arquivo.tipo(r"csv/url.csv", "url", lista_de_url[cont], "cod")
            self.main(lista_de_url[cont], str(tipo), lista_de_ticker[cont])
            cont += 1
            
    def main(self, url, tipo, Ticker, show=False):

        parametros = {
            "-1": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            Cotação atual: {cotação} para {código}.
            Sem mais informações sobre a moeda.
            """,
            "2": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            A cotação atual é {cotação} o código da moeda é {código}.
            No dia de hoje a moeda ficou entre {variações}.
            O rendimento atual é {rendimento_atual}, isso equivale a R${equivalente:.2f} de lucro.
            """,
            "3": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            A cotação atual é {cotação} de {código} e as variações do dia foram entre {variações}.
            """
        }
        Csv = csv()
        try:
            
            Valor = moeda()
            tempo = Horarios()
            data = tempo.data_atual()
            hora = tempo.hora_atual()

            try:
                self.resposta = requests.get(url)
            except:
                Csv.escrever_csv("Url inválida", r"csv/erros.csv", "a")

            tratamento = Tratamento_de_strings()

            if self.resposta.status_code == 200:
                if tipo == "-1" or tipo == "2" or tipo == "3":
                    soup = BeautifulSoup(self.resposta.text, "html.parser")
                    cotação = soup.select_one("div.YMlKec.fxKbKc")
                    self.cotação = Valor.formatar_moeda(tratamento.tratar_dados_de_url(cotação))
                    self.código = Ticker
                    self.rendimento = None
                    self.variações = None
                    self.equivalente = None
                    if tipo == "2" or tipo == "3":
                        variação_do_preço = soup.select("div.P6K39c")
                        rendimentos = variação_do_preço[6]
                        self.rendimento = tratamento.tratar_dados_de_url(rendimentos)
                        self.variações = tratamento.tratar_dados_de_url(variação_do_preço[2])
                        self.equivalente = tratamento.tratar_valores_url(cotação, rendimentos)

                if str(tipo) in parametros and show == True:
                    print(parametros[tipo](cotação=self.cotação, código=self.código,
                                           variações=self.variações, rendimento_atual=self.rendimento,
                                           equivalente=self.equivalente))

                Csv.escrever_csv(conteudo=(self.código, self.cotação,
                                           hora, data),
                                 nome=r"csv/dados_das_cotações.csv", tipo="a"
                                           )
        except (ValueError, TypeError) as e:
            Csv.escrever_csv(conteudo=f"Erro do tipo: {e}", nome=r"erros.csv", tipo="a")

        except Exception as e:
            Csv.escrever_csv(conteudo=f"Erro inesperado: {e}", nome=r"erros.csv", tipo="a")

    def tipo_de_ativo(self, url):
        pontos = str(url[40:])
        número = pontos.find(":")
        return número

if __name__ == "__main__":
    conn = conexão()