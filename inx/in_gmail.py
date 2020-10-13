from __future__ import print_function
import sys
import os.path
import json
from services import gmail_service
import base64
import traceback
from time import time

# config
DATA_STORE = 'io_handler_gmail.json'

try:
    if (not os.path.isfile(DATA_STORE)):
        dataStoreHandler = open(DATA_STORE, 'w')
        json.dump({'lastChecked': str(int(time()) - 7889238)}, dataStoreHandler)
        dataStoreHandler.close()
except:
    traceback.print_exception(*sys.exc_info())

def get():
    try:
        service = gmail_service.buildService()
        messages = service.users().messages().list(userId='me', q='after:' + getLastChecked()).execute()
        print('checking ' + (str(len(messages['messages'])) if 'messages' in messages else '0') + ' new messages')

        if ('messages' in messages):
            filesContents = {}
            for message in messages['messages']:

                msg = service.users().messages().get(userId='me', id=message['id']).execute()

                if ('parts' in msg['payload']):
                    for part in msg['payload']['parts']:

                        filename = part['filename'].split('.')
                        if (filename[len(filename) - 1] in ['xml', 'gz', 'zip']):

                            if 'data' in part['body']:
                                data = part['body']['data']
                            else:
                                attId = part['body']['attachmentId']
                                att = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attId).execute()
                                data = att['data']

                            file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                            filesContents[filename] = file_data
            checkedNow()
            return filesContents
    except:
        traceback.print_exception(*sys.exc_info())

def checkedNow():
    dataStoreHandler = open(DATA_STORE, 'w')
    json.dump({'lastChecked': str(int(time()))}, dataStoreHandler)
    dataStoreHandler.close()

def getLastChecked():
    dataStoreHandler = open(DATA_STORE, 'r')
    dataStore = json.load(dataStoreHandler)
    dataStoreHandler.close()
    return str(dataStore['lastChecked'])
