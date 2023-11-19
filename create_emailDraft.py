import base64
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from gmail_api import create_service
import time

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


def search_emails(query, labels=None):
    # email_messages = []
    next_page_token = None

    message_response = service.users().messages().list(
        userId='me',
        labelIds=labels,
        includeSpamTrash=False,
        q=query,
        maxResults=500
    ).execute()
    email_messages = message_response.get('messages')
    next_page_token = message_response.get('nextPageToken')

    while next_page_token:
        message_response = service.users().messages().list(
            userId='me',
            labelIds=labels,
            q=query,
            maxResults=500,
            includeSpamTrash=False,
            pageToken=next_page_token
        ).execute()
        email_messages.extend(message_response['messages'])
        next_page_token = message_response.get('nextPageToken')
        print('Page Token: {0}'.format(next_page_token))
        time.sleep(0.5)
    return email_messages

def delete_emails(email_results):
  for email_result in email_results:
    service.users().messages().trash(
        userId='me',
        id=email_result['id']
    ).execute()
