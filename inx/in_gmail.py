from services import gmail_service

service = gmail_service.buildService()

def get():
    # dummy info
    print('2 new messages')
    # dummy xml-file list
    return {'test2.xml': '<feedback><feedback>', 'test3.xml': '<feedback><feedback>'}
