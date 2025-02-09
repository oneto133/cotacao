import asyncio
import cloudpickle
import traceback
import pandas as pd
from cotação import main as cot
from enviar_email import enviar_mensagem
from Funções import Tempo
from dados_excel import main as excel
class Programa(Tempo):
    def __init__(self):
        super().__init__()
        
    async def fii(self):
        cotação = cot()
        print("Excel")
        await cotação.programa("fii")

    async def bdr(self):
        cotação = cot()
        print("executado")
        await cotação.programa("bdr")

    async def base_banco(self):
        pass 

    async def main(self):
        if self.Dias_da_semana(True) == 5 or self.Dias_da_semana(True) == 6:
            print("O mercado financeiro não funciona aos fins de semana")
            df = pd.read_csv(r"csv/indice.csv", encoding="latin1")
            data = df.columns[1]
            Hor = Tempo()
            dat = Hor.data_atual()
            if data != dat:
                excel()

        else:    
            await asyncio.gather(self.bdr(), self.fii())

if __name__ == "__main__":
    try:
        programa = Programa()
        asyncio.run(programa.main())
                
    except KeyboardInterrupt:
        with open(r"pkl/mensagem_email.pkl", "rb") as file:
            dados = cloudpickle.load(file)
        print("Finalizado pelo usuário")
        enviar_mensagem(titulo=dados["Finalizado"], mensagem=(dados["mensagem_finalizado"], traceback.format_exc()),
                        mensagem_final=dados["mensagem final"] )

    except:
        with open(r"pkl/mensagem_email.pkl", "rb") as file:
            dados = cloudpickle.load(file)
        print("Ocorreu um erro, vamos finalizar o programa")

        enviar_mensagem(titulo=dados["Erro"], mensagem=(dados["mensagem_erro"], traceback.format_exc()),
                        mensagem_final=dados["mensagem final"])