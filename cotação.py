from bs4 import BeautifulSoup
from Funções import Tratamento_de_strings, csv, Tempo, moeda
from enviar_email import enviar_mensagem
import traceback, cloudpickle, requests, asyncio
import pandas as pd
from time import sleep
from dados_excel import main as Excel

class conexão (csv, Tratamento_de_strings, Tempo, moeda):
    def __init__(self, tipo):

        super().__init__()
        self.ultimo = ["Teste"]
        self.Programa(tipo)
    
    def Programa(self, tipo):
        lista_de_url = []
        lista_de_ticker = []
        ler = self.url(tipo)
        Ticker = self.Ticker(tipo)
        for url in ler:
            lista_de_url.append(url)
        for ticker in Ticker:
            lista_de_ticker.append(ticker)

        cont = 0

        for c in range(0,len(lista_de_url)):
            if self.ultimo[-1] == lista_de_ticker[cont]:
                continue
            else:
                self.ultimo.append(lista_de_ticker[cont])
                tipo = self.tipo(r"csv/url.csv", "url", lista_de_url[cont], "cod")
                self.main(lista_de_url[cont], str(tipo), lista_de_ticker[cont])
                cont += 1
            

    def main(self, url, tipo, Ticker, show=False):
        try:
            self.resposta = requests.get(url)
            self.resposta.raise_for_status()

            if self.resposta.status_code == 200:
                if tipo == "-1" or tipo == "2" or tipo == "3":
                    soup = BeautifulSoup(self.resposta.text, "html.parser")
                    cotação = soup.select_one("div.YMlKec.fxKbKc")
                    self.cotação = self.formatar_moeda(self.tratar_dados_de_url(cotação))
                    self.código = Ticker
                    self.rendimento = None
                    self.variações = None
                    self.equivalente = None
                    self.ultimo_preço = None
                    if tipo == "2" or tipo == "3":
                        variação_do_preço = soup.select("div.P6K39c")
                        try:
                            rendimentos = variação_do_preço[6]
                            self.variações = self.tratar_dados_de_url(variação_do_preço[1])
                            self.ultimo_preço = self.tratar_dados_de_url(variação_do_preço[0])

                        except:
                            rendimentos = "Sem dados"
                            self.variações  = "Sem dados"
                            self.ultimo_preço = "Sem dados ou Erro!"
                        self.rendimento = self.tratar_dados_de_url(rendimentos)
                        self.equivalente = self.tratar_valores_url(cotação, rendimentos)
                        self.ultimo_preço = self.tratar_dados_de_url(variação_do_preço[0])
                parametros = [-1, 2, 3]
                if str(tipo) in parametros and show == True:
                    with open(r"pkl/parametros.pkl", "rb") as file:
                        parametros = cloudpickle.load(file)
                    print(parametros[tipo](cotação=self.cotação, código=self.código,
                                           variações=self.variações, rendimento_atual=self.rendimento,
                                           equivalente=self.equivalente))
                self.escrever_csv(conteudo=(f'"{self.código}", "{self.cotação}",'
                                           f'"{self.hora_atual()}", "{self.data_atual()}", "{self.variações}"'),
                                 nome=r"csv/dados_das_cotações.csv", tipo="a"
                                           )
                
        except (ValueError, TypeError) as e:
            self.escrever_csv(conteudo=f"Erro do tipo: {e}", nome=r"erros.csv", tipo="a")
        except requests.exceptions.HTTPError as e:
                print("Erro HTTP:", e)
        except requests.exceptions.ConnectionError:
            print("Erro de conexão. Verifique a URL ou sua conexão.")
        except requests.exceptions.Timeout:
            print("A requisição expirou. O servidor pode estar lento ou indisponível.")
        except requests.exceptions.RequestException as e:
            print("Erro ao fazer a requisição:", e)
        except Exception as e:
            self.escrever_csv(conteudo=f"Erro inesperado: {e}", nome=r"erros.csv", tipo="a")

class main(Tempo):
    def __init__(self):
        super().__init__()

    async def programa(self, tipo):
        while True:
            hora = self.hora_atual()
            print(hora)
            if int(hora[:2]) < 10 or int(hora[:2]) >= 18:
                if int(hora[:2]) >=18 and int(hora[:2]) <= 22:
                    df = pd.read_csv(r"csv/indice.csv", encoding="latin1")
                    data = df.columns[1]
                    Hor = Tempo()
                    dat = Hor.data_atual()
                    if data != dat:
                        Excel()
                if int(hora[:2]) < 10:
                    tempo = 10 - int(hora[:2])
                    tempo = int(tempo) * 30 * 60
                    print("Fora do horário de negociações, tentarei novamente em breve...")
                    await asyncio.sleep(tempo)
                else:
                    tempo = 5 * 30 * 60
                    print("Fora do horário de negociações, tentarei novamente em breve...")
                    await asyncio.sleep(tempo)
                
            else:
                print("Funcionando normal")
                await self.conn(tipo)
        
        
        
    async def conn(self, tipo):
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self.exec, tipo)
        
    def exec(self, tipo):
        conexão(tipo)


if __name__ == "__main__":
    async def pro():
        app = main()
        await app.programa()
    try:
        asyncio.run(main())
                
    except KeyboardInterrupt:
        with open(r"pkl/mensagem_email.pkl", "rb") as file:
            dados = cloudpickle.load(file)
        print("Finalizado pelo usuário")
        enviar_mensagem(titulo=dados["Finalizado"], mensagem=(dados["mensagem_finalizado"], traceback.format_exc()),
                        mensagem_final=dados["mensagem final"] )
    
    except:
        with open(r"pkl/mensagem_email.pkl", "rb") as file:
            dados = cloudpickle.load(file)
        print("Ocorreu um erro, vamos finalizando o programa")

        enviar_mensagem(titulo=dados["Erro"], mensagem=(dados["mensagem_erro"], traceback.format_exc()),
                        mensagem_final=dados["mensagem final"])