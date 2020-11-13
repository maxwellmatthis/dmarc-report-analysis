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
    print('Usage: python3 add.py [input type]')
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
