from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# Escopo para acessar mensagens
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def autenticar_gmail():
    """
    A autenticação é feita com um arquivo de nome: credentials.json para
    que se possa conseguir realizar o login e ter acesso ao email
    após, se salva os dados da autenticação num arquivo pkl para que não se necessite mais
    do arquivo .json
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)

def listar_mensagens():
    """
    Depois de feita a autenticação, o programa busca as ultimas mensagens da caixa de entrada
    Args:
        service: Recebe a confirmação de acesso

        results: Obtém as ultimas cinco mensagens

        messages: Adiciona as mensagens numa lista chamada 'messages'
    """
    try:
        service = autenticar_gmail()
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])

        if not messages:
            print("Nenhuma mensagem encontrada.")
        else:
            print("Mensagens:")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print(f"- Assunto: {msg['snippet']}")
    except Exception as e:
        import traceback
        t = traceback.format_exc()
        print(f"Erro ao listar mensagens: {e}", t)

if __name__ == '__main__':
    listar_mensagens()
