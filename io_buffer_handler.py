from enum import unique
import os.path
import json

REPORTS_BUFFER_FILE = 'io_handler_buffer.json'

class BufferHandler:
    def __init__(self):
        if (not os.path.isfile(REPORTS_BUFFER_FILE)):
            self.setDefault()
        self.cached = False
        self.buffer = {}


    def read(self):
        # caching
        if (self.cached == False):
            reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'r')
            self.buffer = json.load(reportsBufferHandler)
            reportsBufferHandler.close()
            self.cached = True
        return self.buffer


    def add(self, data):
        fraud = []
        misconfiguration = []
        for record in data:
            if (record['category'] == 'fraud'):
                fraud.append(record)
            elif (record['category'] == 'misconfiguration'):
                misconfiguration.append(record)
        self.merge(fraud, misconfiguration)


    def setDefault(self):
        print('setting default values')
        self.write({
            'fraud': [],
            'misconfiguration': []
        })


    def merge(self, fraud, misconfiguration):
        uniqueFraud = []
        for record in fraud:
            if (record not in self.read()['fraud']):
                uniqueFraud.append(record)
        uniqueMisconfiguration = []
        for record in misconfiguration:
            if (record not in self.read()['fraud']):
                uniqueMisconfiguration.append(record)
        self.write({
            'fraud': self.read()['fraud'] + uniqueFraud,
            'misconfiguration': self.read()['misconfiguration'] + uniqueMisconfiguration,
        })
    

    def write(self, data):
        reportsBufferHandler = open(REPORTS_BUFFER_FILE, 'w')
        json.dump(data, reportsBufferHandler)
        reportsBufferHandler.close()
        self.cached = False
