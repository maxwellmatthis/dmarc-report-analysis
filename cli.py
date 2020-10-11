import sys
from rua_analyzer import analyse
from banner import banner


def printUsage():
    print('Incorrect Usage!')
    print('Usage: python3 cli.py [filepath]')


if __name__ == "__main__":
    banner()
    if (len(sys.argv) == 2):
        records = analyse(open(sys.argv[1], 'r').read())
        print('showing analysis for ' +
              str(len(records)) + ' records in ' + sys.argv[1] + '\n')
        for record in records:
            for key in record:
                print(key + ': ' + str(record[key]))
            print('')
    else:
        printUsage()
