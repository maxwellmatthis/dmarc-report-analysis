from __future__ import print_function
import sys
import os.path
import json
from rua_analyzer import analyze
from banner import banner
import io_buffer_handler
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# from email.generator import Generator
import base64
import traceback
from time import time


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# config
CONFIG_FILE = 'io_handler_gmail.config.json'
DATA_STORE = 'io_handler_gmail.json'


class Handler:
    def __init__(self, mode):
        if (not os.path.isfile(CONFIG_FILE)):
            configFileHandle = open(CONFIG_FILE, 'w')
            json.dump({
                # TODO
                'sendReportsImmediately': False, # input('Do you want to receive reports as they come in? (yes/no) ') in ('yes', 'y', 'Yes', 'Y'),
                'sendReportsTo': False # input('Which email address should reports be sent to? ')
            }, configFileHandle)
            print(
                'You can change these setting any time in io_handler_gmail.config.json.')
            configFileHandle.close()

        if (not os.path.isfile('credentials.json')):
            sys.exit('FATAL: "credentials.json" not found! You can enable Gmail API and download your credentials.json file by going here: https://console.developers.google.com/apis/library/gmail.googleapis.com?q=gmail')

        configFileHandle = open(CONFIG_FILE, 'r')
        self.CONFIG = json.load(configFileHandle)
        configFileHandle.close()
        print('Config:')
        for key in self.CONFIG:
            print(key + ': ' + str(self.CONFIG[key]))
        print('')

        self.buildService()
        if (mode == 'get'):
            self.checkForNew()
        elif (mode == 'report'):
            self.sendReport()

    def buildService(self):
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
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)

        self.ownMail = self.service.users().getProfile(
            userId='me').execute()['emailAddress']
        print('successfully logged into ' + self.ownMail + '!\n')
        return

    def checkForNew(self):
        try:
            if (not os.path.isfile(DATA_STORE)):
                dataStoreHandler = open(DATA_STORE, 'w')
                json.dump({'lastChecked': str(int(time()) - 7889238)}, dataStoreHandler)
                dataStoreHandler.close()
            dataStoreHandler = open(DATA_STORE, 'r')
            dataStore = json.load(dataStoreHandler)
            dataStoreHandler.close()

            messages = self.service.users().messages().list(
                userId='me', q='after:' + dataStore['lastChecked']).execute()

            print('checking ' + (str(len(messages['messages'])) if 'messages' in messages else '0') + ' new messages')

            if ('messages' in messages):
                BufferHandler = io_buffer_handler.BufferHandler()

                for message in messages['messages']:
                    msg = self.service.users().messages().get(
                        userId='me', id=message['id']).execute()

                    if ('parts' in msg['payload']):
                        for part in msg['payload']['parts']:
                            filename = part['filename'].split('.')
                            if (filename[len(filename) - 1] == 'xml'):
                                if 'data' in part['body']:
                                    data = part['body']['data']
                                else:
                                    attId = part['body']['attachmentId']
                                    att = self.service.users().messages().attachments().get(
                                        userId='me', messageId=message['id'], id=attId).execute()
                                    data = att['data']

                                file_data = base64.urlsafe_b64decode(
                                    data.encode('UTF-8'))
                                BufferHandler.add(analyze(file_data))

                dataStoreHandler = open(DATA_STORE, 'w')
                json.dump({'lastChecked': str(int(time()))}, dataStoreHandler)
                dataStoreHandler.close()

                # TODO
                if (self.CONFIG['sendReportsImmediately']):
                    self.service.users().messages().send(
                        userId='me', body=self.createMessage('Immediate DMARC Failure Report', '<h1>Likely Fraud<h1>' + self.convertRecordsToHTML(BufferHandler.read()['fraud']) + '<h1>Misconfiguration</h1>' + self.convertRecordsToHTML(BufferHandler.read()['misconfiguration'])))
        except:
            traceback.print_exception(*sys.exc_info())

    def sendReport(self):
        # TODO
        print('This feature is being developed')
        return
        try:
            BufferHandler = io_buffer_handler.BufferHandler()

            self.service.users().messages().send(
                userId='me', body=self.createMessage('DMARC Failure Report', '<h1>Likely Fraud<h1>' + self.convertRecordsToHTML(BufferHandler.read()['fraud']) + '<h1>Misconfiguration</h1>' + self.convertRecordsToHTML(BufferHandler.read()['misconfiguration'])))
        except:
            traceback.print_exception(*sys.exc_info())

    def convertRecordsToHTML(self, records):
        if (not records):
            return '<div>no records<div>'
        else:
            allHTML = '<div>'
            for record in records:
                recordHTML = '<div>'
                for key in record:
                    recordHTML += '<span>' + key + \
                        ': ' + str(record[key]) + '</span>'
                recordHTML += '</div>'
                allHTML += recordHTML
            allHTML += '</div>'
            return allHTML

    def createMessage(self, subject, content):
         # TODO MIMEText
        message = MIMEText(content, 'html')
        message['to'] = self.CONFIG['sendReportsTo']
        message['from'] = self.ownMail
        message['subject'] = subject
        # message['cc'] = cc
        return {'raw': base64.urlsafe_b64encode(message.as_string())}


def printUsage():
    print('Incorrect Usage!')
    print('# get new reports from inbox')
    print('$ python3 io_handler_gmail.py get')
    print('# send all collected report data and reset')
    print('$ python3 io_handler_gmail.py report')


if __name__ == "__main__":
    banner()
    if (len(sys.argv) >= 2):
        if (sys.argv[1] == 'get'):
            Handler('get')
        elif (sys.argv[1] == 'report'):
            Handler('report')
        else:
            printUsage()
    else:
        printUsage()
