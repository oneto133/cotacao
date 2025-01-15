import json

def lambda_to_str(func):
    return func.__code__.co_code



parametros = {
            "-1": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            Cotação atual: {cotação} para {código}.
            Sem mais informações sobre a moeda.
            """,
            "2": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            A cotação atual é {cotação} o código da moeda é {código}.
            No dia de hoje a moeda ficou entre {variações}.
            O rendimento atual é {rendimento_atual}, isso equivale a R${equivalente:.2f} de lucro.
            """,
            "3": lambda cotação, código, variações, rendimento_atual, equivalente: f"""
            A cotação atual é {cotação} de {código} e as variações do dia foram entre {variações}.
            """
        }   

dicionario_serializado = {k: {'func_str': str(v)} for k, v in parametros.items()}
with open("parametros.json", "w") as file:
    json.dump(dicionario_serializado, file, indent=4)