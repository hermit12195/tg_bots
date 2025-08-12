import logging
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/documents']


def get_docs_service():
    """
    Authenticates and returns the Google Docs API service instance.

    - Checks for existing credentials in 'token.json'.
    - Refreshes the token if expired.
    - If no valid credentials are found, initiates OAuth flow using 'credentials.json'.
    - Saves refreshed or new credentials to 'token.json'.

    Returns:
        googleapiclient.discovery.Resource: An authorized Google Docs API service instance.
    """
    try:
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if creds and creds.expired and creds.refresh_token:
            from google.auth.transport.requests import Request
            creds.refresh(Request())

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        if not creds or not creds.valid:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(script_dir, 'credentials.json')
            flow = InstalledAppFlow.from_client_secrets_file(file_path, SCOPES)
            creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('docs', 'v1', credentials=creds)
        return service
    except Exception as e:
        logging.error({e})


def append_text_to_doc(document_id, text):
    """
    Appends the given text to the end of a Google Docs document.

    Args:
        document_id (str): The ID of the Google Docs document.
        text (str): The text to append to the document.

    Returns:
        None
    """
    try:
        service = get_docs_service()

        doc = service.documents().get(documentId=document_id).execute()
        end_index = doc.get('body').get('content')[-1].get('endIndex')

        requests = [
            {
                'insertText': {
                    'location': {
                        'index': end_index - 1,
                    },
                    'text': text + "\n"
                }
            }
        ]

        service.documents().batchUpdate(documentId=document_id, body={'requests': requests}).execute()
    except Exception as e:
        logging.error({e})
