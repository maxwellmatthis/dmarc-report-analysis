from services import gmail_service

service = gmail_service.buildService()

def send(records):
    # dummy info
    print('sending report to address@example.com')
