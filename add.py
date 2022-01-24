#!/usr/bin/python3

from banner import banner
import sys
import os.path

BUFFER_FOLDER = 'buffer'


def addToBuffer(filesContents):
    if (not os.path.isdir(BUFFER_FOLDER)):
        os.mkdir(BUFFER_FOLDER)

    if (filesContents is not None and len(filesContents) >= 1):
        for file in filesContents:
            with open(os.path.join(BUFFER_FOLDER, file), 'wb') as f:
                f.write(filesContents[file])
        print('added ' + str(len(filesContents)) + ' ' +
              ('files' if (len(filesContents) > 1) else 'file') + ' to the buffer')
    else:
        print('no new files to add to the buffer')


def printUsage():
    print('Usage: python3 add.py [input type] [options?]')
    print('input types: gmail')
    print('options: batch_size=n')


if __name__ == "__main__":
    banner()
    if (len(sys.argv) >= 2):
        filesContents = None
        if (sys.argv[1] == 'gmail'):
            from inputs import in_gmail
            filesContents = in_gmail.get(sys.argv[2] if str(
                sys.argv[2]).split('=')[0] == 'batch_size' else str(100))
        else:
            print('Incorrect Usage!')
            printUsage()
        addToBuffer(filesContents)
    else:
        printUsage()
