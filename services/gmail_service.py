import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# credentials file from gmail api
SECRETS_FILE = 'credentials.json'

def buildService():

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    creds = None
    if (os.path.exists('token.pickle')):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if (not creds or not creds.valid):
        if (creds and creds.expired and creds.refresh_token):
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    print('successfully logged into ' + service.users().getProfile(userId='me').execute()['emailAddress'] + '!')

    # return service object
    return service

if __name__ == "__main__":
    print('Attempting to build Gmail API Service...')
    buildService()
