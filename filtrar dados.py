import pandas as pd

# Carregar os dados
df = pd.read_csv("csv/url.csv", encoding="latin")
dados = pd.read_csv("csv/remover.csv", encoding="latin1")

# Extrair os códigos a serem removidos
codigos_remover = dados['Ticker'].tolist()

# Filtrar o DataFrame df para manter apenas as linhas que NÃO estão na lista de códigos
df_filtrado = df[~df['codigo'].isin(codigos_remover)]

# Salvar o DataFrame filtrado
df_filtrado.to_csv("csv/url_filtrado.csv", index=False)