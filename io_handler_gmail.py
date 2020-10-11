from __future__ import print_function
import sys
import os.path
import json
import rua_analyzer
from banner import banner
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
REPORTS_BUFFER_FILE = 'io_handler_buffer.json'


class Handler:
    def __init__(self, mode):
        if (not os.path.isfile(CONFIG_FILE)):
            configFileHandle = open(CONFIG_FILE, 'w')
            json.dump({
                'sendReportsImmediately': input('Do you want to receive reports as they come in? (yes/no)') in ('yes', 'y', 'Yes', 'Y'),
                'sendReportsTo': input('Which email address should reports be sent to? ')
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

    def buildService(self):
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if (os.path.exists('token.pickle')):
            with open('token.pickle', 'rb') as token:
                CREDS = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if (not CREDS or not CREDS.valid):
            if (CREDS and CREDS.expired and CREDS.refresh_token):
                CREDS.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                CREDS = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(CREDS, token)

        self.service = build('gmail', 'v1', credentials=CREDS)

        self.ownMail = self.service.users().getProfile(  # pylint: disable=maybe-no-member
            userId='me').execute()['emailAddress']
        print('successfully logged into ' + self.ownMail + '!\n')

        return

    def checkForNew(self):
        try:
            if (not os.path.isfile(REPORTS_BUFFER_FILE)):
                self.defaultBufferFile()
            
            reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'r')
            reportsBuffer = json.load(reportsBufferHandler)
            
            messages = self.service.users().messages().list(  # pylint: disable=maybe-no-member
                userId='me', q='after:' + reportsBuffer['lastChecked']).execute()

            analysis = {}
            fraud = []
            misconfiguration = []

            for message in messages['messages']:
                msg = self.service.users().messages().get(  # pylint: disable=maybe-no-member
                    userId='me', id=message['id']).execute()

                for part in msg['payload']['parts']:
                    filename = part['filename']
                    if (filename.split('.')[len(filename) - 1] == 'xml'):
                        if 'data' in part['body']:
                            data = part['body']['data']
                        else:
                            attId = part['body']['attachmentId']
                            att = self.service.users().messages().attachments().get(  # pylint: disable=maybe-no-member
                                userId='me', messageId=message['id'], id=attId).execute()
                            data = att['data']

                        file_data = base64.urlsafe_b64decode(
                            data.encode('UTF-8'))
                        analysis = rua_analyzer.analyse(file_data)

                        for record in analysis:
                            if (record['category'] == 'fraud'):
                                fraud.append(record)
                            elif (record['category'] == 'misconfiguration'):
                                misconfiguration.append(record)

            reportsBufferHandler.close()

            reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'w')
            json.dump({
                'lastChecked': str(int(time())),
                'fraud': reportsBuffer['fraud'] + fraud,
                'misconfiguration': reportsBuffer['misconfiguration'] + misconfiguration
            }, reportsBufferHandler)
            reportsBufferHandler.close()

            if (self.CONFIG['sendReportsImmediately']):
                self.service.users().messages().send(  # pylint: disable=maybe-no-member
                    userId='me', body=self.createMessage('Immediate DMARC Failure Report', '<h1>Likely Fraud<h1>' + self.convertRecordsToHTML(fraud) + '<h1>Misconfiguration</h1>' + self.convertRecordsToHTML(misconfiguration)))

        except:
            traceback.print_exception(*sys.exc_info())

    def sendReport(self):
        try:
            if (not os.path.isfile(REPORTS_BUFFER_FILE)):
                self.defaultBufferFile()

            reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'r')
            reportsBuffer = json.load(reportsBufferHandler)
            reportsBufferHandler.close()

            self.service.users().messages().send(  # pylint: disable=maybe-no-member
                userId='me', body=self.createMessage('DMARC Failure Report', '<h1>Likely Fraud<h1>' + self.convertRecordsToHTML(reportsBuffer['fraud']) + '<h1>Misconfiguration</h1>' + self.convertRecordsToHTML(reportsBuffer['misconfiguration'])))

            reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'w')
            json.dump({
                'lastChecked': reportsBuffer['lastChecked'],
                'fraud': {},
                'misconfiguration': {}
            }, reportsBufferHandler)
            reportsBufferHandler.close()

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

    def createMessage(self, subject, message_text):
        message = MIMEText(message_text, 'html') # HERE
        message['to'] = self.CONFIG['sendReportsTo']
        message['from'] = self.ownMail
        message['subject'] = subject
        # message['cc'] = cc
        return {'raw': base64.urlsafe_b64encode(message.as_string())}

    def defaultBufferFile(self):
        reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'w')
        json.dump({
            'lastChecked': '1600000000',
            'fraud': {},
            'misconfiguration': {}
        }, reportsBufferHandler)
        reportsBufferHandler.close()


def printUsage():
    print('Incorrect Usage!')
    print('# get new reports from inbox')
    print('$ python3 io_handler_gmail.py get')
    print('# send all collected report data and reset')
    print('$ python3 io_handler_gmail.py report')


if __name__ == "__main__":
    banner()
    if (len(sys.argv) >= 1):
        if (sys.argv[1] == 'get'):
            Handler('get')
        elif (sys.argv[1] == 'report'):
            Handler('report')
        else:
            printUsage()
    else:
        printUsage()
