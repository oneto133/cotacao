import smtplib
import email.message

def enviar_mensagem(email_remetente='rodriguesarmando225@gmail.com',
                    email_destinatario='allmyfilesondrive@gmail.com',
                    titulo=None,
                    senha_de_app="nvezhiuvnucwvcde",
                    mensagem=None,
                    mensagem_final=None):
  """
  Envio de email
  será nescessário realizar login com a senha de app e email
  também forneça o titulo, e o corpo da mensagem, também se pode adicionar
  uma linha final da mensagem.

  Args:
    email_remetente (str): será o email de quem vai enviar a mensagem

    email_destinatário (str): É o email de quem vai receber a mensagem
    
    titulo (str): Seja criatívo, use um título chamativo!
    
    senha_de_app (str): A senha de app é importante pois, assim o usuário não precisa usar de sua senha pessoal se tornando vunerável, para saber mais sobre abra as configurações do gmail, em segurança, digite senha de app e crie a sua nova senha, você precisará de uma conta verificada em duas etapas.

    mensagem (str): A mensagem a ser enviada ao destinatário
    
    mensagem_final (str):  A ultima linha de mensagem

  Returns:
    None: apenas um print indicando que a mensagem foi enviada com sucesso...
  """
  corpo_mensagem = f"""
  <p>{mensagem}<p>
  <p>{mensagem_final}<p>
  """
  msg = email.message.Message()
  msg['Subject'] = titulo
  msg['From'] = email_remetente
  msg['To'] = email_destinatario
  password = senha_de_app
  msg.add_header('Content-Type', 'text/html')
  msg.set_payload(corpo_mensagem)

  s = smtplib.SMTP('smtp.gmail.com: 587')
  s.starttls()
  s.login(msg['From'], password)
  s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))


if __name__ == "__main__":
    enviar_mensagem()
    print("Email enviado")