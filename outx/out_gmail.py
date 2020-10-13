from services import gmail_service

service = gmail_service.buildService()

def send(records):
    # dummy info
    print('sending report to address@example.com')


    # def convertRecordsToHTML(self, records):
    #     if (not records):
    #         return '<div>no records<div>'
    #     else:
    #         allHTML = '<div>'
    #         for record in records:
    #             recordHTML = '<div>'
    #             for key in record:
    #                 recordHTML += '<span>' + key + \
    #                     ': ' + str(record[key]) + '</span>'
    #             recordHTML += '</div>'
    #             allHTML += recordHTML
    #         allHTML += '</div>'
    #         return allHTML

    # def createMessage(self, subject, content):
    #     # TODO MIMEText
    #     message = MIMEText(content, 'html')
    #     message['to'] = self.CONFIG['sendReportsTo']
    #     message['from'] = self.ownMail
    #     message['subject'] = subject
    #     # message['cc'] = cc
    #     return {'raw': base64.urlsafe_b64encode(message.as_string())}

    # def sendReport(self):
    #     # TODO
    #     try:
    #         BufferHandler = io_buffer_handler.BufferHandler()

    #         self.service.users().messages().send(
    #             userId='me', body=self.createMessage('DMARC Failure Report', '<h1>Likely Fraud<h1>' + self.convertRecordsToHTML(BufferHandler.read()['fraud']) + '<h1>Misconfiguration</h1>' + self.convertRecordsToHTML(BufferHandler.read()['misconfiguration'])))
    #     except:
    #         traceback.print_exception(*sys.exc_info())
