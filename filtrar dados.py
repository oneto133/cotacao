import pandas as pd

df = pd.read_csv(r"csv/dados_das_cotações.csv", encoding="latin1")

url = pd.read_csv(r"csv/url.csv", encoding="latin1")

lista2 = []
lista1 = []
excluido = []
for valor in df["codigo"]:
    lista1.append(valor)

for valor in url["codigo"]:
    lista2.append(valor)

for valor in lista2:
    if valor not in lista1:
        excluido.append(valor)

print(len(excluido))
print(excluido)