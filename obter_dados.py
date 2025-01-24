import pandas as pd
from Funções import csv

class dados():
    def __init__(self, codigo="MXRF11", data_inicial=str(), data_final=str(), arquivo="csv/dados_das_cotações.csv"):
      
        self.df = pd.read_csv(arquivo, encoding="latin1")

        self.codigo = codigo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.main()

    def main(self):

        filtro = (
        self.df["codigo"] == self.codigo) & (
        self.df["data"] >= f' "{self.data_inicial}"') & (
        self.df["data"] <= f' "{self.data_final}"')
        preço = self.df.loc[filtro, "preco"]
        lista = []
        variacoes_percentuais = []
        variacao_moeda = []
        soma = 0

        for valor in preço:
            valor = float(valor.replace("R$", "").replace('"', ""))
            soma += valor
            lista.append(valor)
        preço_medio = "{:.2f}".format(soma / len(preço))

        for i in range(1, len(lista)):
            valor_anterior = (lista[i - 1])
            valor_atual = (lista[i])
            variacao = ((valor_atual - valor_anterior) / valor_anterior) * 100
            variacoes_percentuais.append(variacao)
        
        for i in range(1, len(lista)):
            valor_anterior = (lista[i - 1])
            valor_atual = (lista[i])
            variacao = (valor_atual - valor_anterior)
            variacao_moeda.append(variacao)

        preço_medio = float(preço_medio)

        valor = (lista[-1] - preço_medio)

        if lista[-1] < preço_medio:
            print(self.codigo)
            print(f"Abaixo da média R${valor:.2f}")
            print(f"Preço médio: R$",preço_medio)
            print(f"Valor mínimo no período: R${min(lista):.2f}\nMáxima do periodo: R${max(lista)}")
            print(f"Ultimo valor R${lista[-1]}")
            print("*="*20)
            
        
        elif lista[-1] == preço_medio:
            pass
            # print("O preço está na sua média")
        else:
            pass
            # print(f"Acima média R${valor:.2f}")
class main:
    def __init__(self, Unitário=False, Vários=False):
        if Unitário:
            self.unitário()
        elif Vários:
            self.todos()
            
    def unitário(self):
        print("Aqui")
        dados(data_final="17/01/2025", data_inicial="01/01/2025", codigo="MXRF11")
        
    def todos(self):
        arquivo = csv()
        ticker = arquivo.ler_csv("csv/dados_das_cotações.csv", "codigo", ",")
        codigo = []
    
        for valor in ticker:
            codigo.append(valor)
            dados(data_final="23/01/2025", data_inicial="01/01/2025", codigo=valor)
            

if __name__ == "__main__":
    main(Vários=True)

 
