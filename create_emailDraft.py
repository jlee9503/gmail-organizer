import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from gmail_api import create_service

CLIENT_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

def gmail_send_message(recipient: str, sender: str, msg: str):

  try:
    message = EmailMessage()

    message.set_content("This is a test mail")

    message["To"] = recipient
    message["From"] = sender
    message["Subject"] = msg

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message


# if __name__ == "__main__":
#   gmail_send_message()
