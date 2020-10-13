from banner import banner
import sys
import os.path

BUFFER_FOLDER = 'buffer'

def addToBuffer(filesContents):
    for file in filesContents:
        bufferFileHandler = open(os.path.join(BUFFER_FOLDER, file), 'w')
        bufferFileHandler.write(filesContents[file])
        bufferFileHandler.close()

def printUsage():
    print('Usage: python3 get.py [input type]')
    print('input types: gmail')

if __name__ == "__main__":
    banner()
    if (len(sys.argv) == 2):
        filesContents = None
        if (sys.argv[1] == 'gmail'):
            from inx import in_gmail
            filesContents = in_gmail.get()
        else:
            print('Incorrect Usage!')
            printUsage()
        addToBuffer(filesContents)
    else:
        printUsage()
