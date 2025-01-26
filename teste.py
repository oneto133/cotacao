import win32com.client as win32

excel = win32.gencache.EnsureDispatch('Excel.Application')
wb = excel.Workbooks.Open(r'C:\Users\rodri\OneDrive\Documentos\Base.xlsx')
wb.Close(SaveChanges=True)  # Fecha o arquivo sem salvar
excel.Quit()