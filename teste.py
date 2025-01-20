import cloudpickle
import traceback


dicionario = {
    "Finalizado": "Programa finalizado pelo usuário",
    "mensagem_finalizado": f"""Olá, senhor Neto, aqui é seu assistente, o seu programa foi finalizado pelo usuário.
Vou tentar anexar o traceback nesse e-mail, espero que seja possível vê-lo... \n \n \n \n
""",
    "mensagem final": "Atenciosamente, M.I.A.S.M!",
    "Erro": "Ocorreu um erro na execução do programa",
    "mensagem_erro": f"""Olá, senhor Neto, aqui é seu assistente, o seu programa foi finalizado por algum erro.
Vou tentar anexar o erro nesse e-mail, espero que seja possível vê-lo... 
"""
}

with open("pkl/mensagem_email.pkl", "wb") as file:
    cloudpickle.dump(dicionario, file)