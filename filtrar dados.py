import pandas as pd

df = pd.read_csv(r"csv/dados_das_cotações.csv", encoding="latin1")

filtro = (
        df["codigo"] == "PETR4") & (
        df["data"] >= f' "{"01/01/2025"}"') & (
        df["data"] <= f' "{"05/01/2025"}"')

preço = df.loc[filtro, "preco"]

for valor in preço:
    print(len(valor))