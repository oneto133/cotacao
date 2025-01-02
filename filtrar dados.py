import pandas as pd

df = pd.read_csv(r"csv/url.csv", encoding="latin1")

df.drop_duplicates(keep="first", subset="codigo", inplace=True)

df.to_csv("url.csv", index=False)
