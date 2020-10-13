from banner import banner
import sys
import os.path
from parser import rua_parser

BUFFER_FOLDER = 'buffer'

def query(params, records):
    lastRecords = records
    filteredRecords = []

    print('query: ' + str(', '.join(params)) + '\n')

    for param in params:
        try:
            parts = param.split('=')
            key = parts[0]
            value = parts[1]
        except:
            print('Incorrect Usage!')
            printUsage()
            return

        for record in lastRecords:
            if (key in record and str(record[key]) == str(value)):
                filteredRecords.append(record)

        lastRecords = filteredRecords
        filteredRecords = []

    return lastRecords

def loadBuffer():
    parsed = []

    for file in os.listdir(BUFFER_FOLDER):
        if (os.path.isfile(os.path.join(BUFFER_FOLDER, file)) and file.split('.')[len(file.split('.')) - 1] == 'xml'):
            bufferFileHandler = open(os.path.join(BUFFER_FOLDER, file), 'r')
            parsed = parsed + rua_parser.parse(bufferFileHandler.read())
            bufferFileHandler.close()

    return parsed

def printUsage():
    print('Usage: python3 select.py [output type] [optional: query, query...]')
    print('output types: cli, gmail')
    print('query syntax: key=value')

if __name__ == "__main__":
    banner()
    if (len(sys.argv) >= 2):
        if (sys.argv[1] == 'cli' or sys.argv[1] == 'gmail'):
            records = loadBuffer()
            if (len(sys.argv) >= 3):
                records = query(sys.argv[2:len(sys.argv)], records)

            if (sys.argv[1] == 'cli'):
                from outx import out_cli
                out_cli.printOut(records)
            elif (sys.argv[1] == 'gmail'):
                from outx import out_gmail
                out_gmail.send(records)
        else:
            print('Incorrect Usage!')
            printUsage()
    else:
        printUsage()
