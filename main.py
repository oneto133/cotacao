from bs4 import BeautifulSoup
import requests
from Funções import Tratamento_de_strings, csv, Horarios, moeda
from enviar_email import enviar_mensagem
import traceback
from time import sleep
import cloudpickle

class conexão(csv, Tratamento_de_strings, Horarios, moeda):
    def __init__(self):
        super().__init__()
        lista_de_url = []
        lista_de_ticker = []
        ler = self.ler_csv(r"csv/url.csv", "url")
        Ticker = self.ler_csv(r"csv/url.csv", "codigo")
        for url in ler:
            lista_de_url.append(url)
        for ticker in Ticker:
            lista_de_ticker.append(ticker)
        cont = 0
        for c in range(0,len(lista_de_url)):
            tipo = self.tipo(r"csv/url.csv", "url", lista_de_url[cont], "cod")
            self.main(lista_de_url[cont], str(tipo), lista_de_ticker[cont])
            cont += 1

    def main(self, url, tipo, Ticker, show=False):

        with open(r"pkl/parametros.pkl", "rb") as file:
            parametros = cloudpickle.load(file)

        try:
            data = self.data_atual()
            hora = self.hora_atual()
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

                if str(tipo) in parametros and show == True:
                    print(parametros[tipo](cotação=self.cotação, código=self.código,
                                           variações=self.variações, rendimento_atual=self.rendimento,
                                           equivalente=self.equivalente))

                self.escrever_csv(conteudo=(f'"{self.código}", "{self.cotação}",'
                                           f'"{hora}", "{data}", "{self.variações}"'),
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


if __name__ == "__main__":
    
    try:
        while True:
            tempo = Horarios()
            hora = tempo.hora_atual()
            print(hora)
            if int(hora[:2]) < 10 or int(hora[:2]) >= 18:
                if int(hora[:2]) < 10:
                    tempo = 10 - int(hora[:2])
                    tempo = int(tempo) * 30 * 60
                    print("Fora do horário de negociações, tentarei novamente em breve...")
                    sleep(tempo)
                else:
                    tempo = 5 * 30 * 60
                    print("Fora do horário de negociações, tentarei novamente em breve...")
                    sleep(tempo)
                
            else:
                print("Funcionando normal")
                conn = conexão()
                
    except KeyboardInterrupt:
        print("Finalizado pelo usuário")
        enviar_mensagem(titulo="Programa finalizado!", mensagem=f"""
Olá, senhor Neto, aqui é seu assistente, o seu programa foi finalizado pelo usuário.
Vou tentar anexar o traceback nesse e-mail, espero que seja possível vê-lo... \n \n \n \n                        
"{traceback.format_exc()}"

""", mensagem_final="Atenciosamente, M.I.A.S.M!")
    except:
        print("Ocorreu um erro, vamos finalizando o programa")

        enviar_mensagem(titulo="Programa finalizado!", mensagem=f"""
Olá, senhor Neto, aqui é seu assistente, o seu programa foi finalizado por algum erro.
Vou tentar anexar o erro nesse e-mail, espero que seja possível vê-lo... 
"{traceback.format_exc()}"

""", mensagem_final="Atenciosamente, M.I.A.S.M!")
