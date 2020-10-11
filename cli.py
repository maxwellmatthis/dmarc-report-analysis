import sys
from rua_analyzer import analyze
from banner import banner
import io_buffer_handler


def printUsage():
    print('Incorrect Usage!')
    print('# analyze')
    print('Usage: python3 cli.py analyze [filepath]')
    print('# show a report')
    print('Usage: python3 cli.py report')


if __name__ == "__main__":
    banner()
    if (len(sys.argv) >= 2):
        BufferHandler = io_buffer_handler.BufferHandler()
        if (len(sys.argv) == 3 and sys.argv[1] == 'analyze'):
            analysis = analyze(open(sys.argv[2], 'r').read())
            BufferHandler.add(analysis)
            print('showing analysis for ' +
                str(len(analysis)) + ' new records in ' + sys.argv[2] + '\n')
            for record in analysis:
                for key in record:
                    print('  ' + key + ': ' + str(record[key]))
                print('')
        elif (sys.argv[1] == 'report'):
            print('showing all analyzes\n')

            print('LIKELY FRAUD')
            if (len(BufferHandler.read()['fraud']) == 0):
                print('  no fraud')
            for record in BufferHandler.read()['fraud']:
                for key in record:
                    print('  ' + key + ': ' + str(record[key]))
                print('')

            print('MISCONFIGURATION')
            if (len(BufferHandler.read()['misconfiguration']) == 0):
                print('  no misconfigurations')
            for record in BufferHandler.read()['misconfiguration']:
                for key in record:
                    print('  ' + key + ': ' + str(record[key]))
                print('')
        else:
            printUsage()
    else:
        printUsage()
