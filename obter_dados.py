import pandas as pd

class dados():
    def __init__(self, codigo="B3SA3", data_inicial=str(), data_final=str(), arquivo="csv/dados_das_cotações.csv"):
      
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
        hora = self.df.loc[filtro, "hora"]

        lista_hora = []
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

        print("Hora: ")

        for valor in hora:
            lista_hora.append(valor)

        for valor in lista_hora:
            print(valor, end=", ")

        print("")
        print("Valores percentuais: ")

        for valor in variacoes_percentuais:
            print(f"{valor:.2f}%", end=", ")
        
        for i in range(1, len(lista)):
            valor_anterior = (lista[i - 1])
            valor_atual = (lista[i])
            variacao = (valor_atual - valor_anterior)
            variacao_moeda.append(variacao)
        print()
        print("Variação em R$: ")
        for valor in variacao_moeda:
            if valor == 0:
                pass
            elif str(valor)[0] == "-":
                pass
            else:
                valor = "+" + str(valor)[:4]
            print(f"R${valor}", end=", ")
        print("")

        print(f"Preço médio: ")
        print(f"R${preço_medio}, valor mínimo no período R${min(lista)}, máxima do periodo R${max(lista)}")
        print(f"Ultimo valor {lista[-1]}")


if __name__ == "__main__":
    dados(data_final="02/01/2025", data_inicial="02/01/2025", codigo="PETR4")
 