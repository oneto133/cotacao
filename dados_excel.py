import openpyxl
import pandas as pd
from Funções import Horarios
import shutil


class main(Horarios):
    def __init__(self):
        super().__init__()
        self.arquivos()

    def arquivos(self):
        df = pd.read_csv(r'csv/indice.csv')
        origem = r"C:\Users\rodri\OneDrive\Documentos\Banco Gênio.xlsx"
        destino = r"C:\Users\rodri\OneDrive\Documentos\Banco_gênio_temp.xlsx"
        shutil.copy2(origem, destino)
        arq = openpyxl.load_workbook(r"C:\Users\rodri\OneDrive\Documentos\Banco_gênio_temp.xlsx", data_only=True)
        base = openpyxl.load_workbook(r"C:\Users\rodri\OneDrive\Documentos\Base.xlsx")
        self.programa(df, arq, base)

    def programa(self, df, arq, base):

        linha_destino = int(df.columns[0])
        coluna_destino = 1
        Financeiro = arq["Financeiro"]
        Banco_de_dados = base["Base"]
        Intervalo = ["A5:F5", "I6:P6"]
        Dados = []

        for intervalo in Intervalo:
            for row in Financeiro[intervalo]:
                dado = [cell.value for cell in row]
                Dados.extend(dado)


        for coluna, valor in enumerate(Dados):
            Banco_de_dados.cell(row=linha_destino, column=coluna_destino + coluna, value=valor)

        Banco_de_dados.cell(row=linha_destino, column=coluna+2, value=self.data_atual())
        Banco_de_dados.cell(row=linha_destino, column=coluna+3, value=self.hora_atual())

        with open("csv/indice.csv", "w") as file:
            file.write(f'"{linha_destino+1}",{self.data_atual()},{self.hora_atual()}')

        base.save(r"C:\Users\rodri\OneDrive\Documentos\Base.xlsx")
        print("executado")

if __name__ == "__main__":
    df = pd.read_csv(r"csv/indice.csv", encoding="latin1")
    data = df.columns[1]
    Hor = Horarios()
    dat = Hor.data_atual()
    if data != dat:
        main()
    else:
        print("Não executado!")