import os
import json

TRUSTFILE = 'trust.json'

class TrustChecker:
    def __init__(self):
        if (not os.path.isfile(TRUSTFILE)):
            open(TRUSTFILE, 'w').write('{}')
        trustFileHandle = open(TRUSTFILE, 'r')
        self.trust = json.load(trustFileHandle)
        trustFileHandle.close()

    def getIsTrusted(self, domain, ip):
        if (domain in self.trust and
            type(self.trust[str(domain)]) is list and
                ip in self.trust[domain]):
            return True
        else:
            return False


def add(ip, domain):
    if (not os.path.isfile(TRUSTFILE)):
        open(TRUSTFILE, 'w').write('{}')
        print('created TRUSTFILE')

    contents = json.load(open(TRUSTFILE, 'r'))
    if (domain in contents and type(contents[domain]) is list):
        if (not ip in contents[domain]):
            contents[domain].append(ip)
            print('added ' + ip + ' to ' + domain)
        else:
            print(ip + ' is already trusted on ' + domain)
    else:
        contents[domain] = [ip]
        print('added ' + ip + ' to ' + domain)

    trustFileHandle = open(TRUSTFILE, 'w')
    json.dump(contents, trustFileHandle)
    trustFileHandle.close()


def remove(ip, domain):
    if (os.path.isfile(TRUSTFILE)):
        contents = json.load(open(TRUSTFILE, 'r'))
        if (domain in contents and type(contents[domain]) is list):
            if (not ip in contents[domain]):
                contents[domain].remove(ip)
                print('removed ' + ip + ' from ' + domain)
            else:
                print(ip + ' wasn\'t not trusted on ' + domain)
        else:
            print(domain + ' doesn\'t have any trusted ips')

        trustFileHandle = open(TRUSTFILE, 'w')
        json.dump(contents, trustFileHandle)
        trustFileHandle.close()

    else:
        print('ERROR: no TRUSTFILE')
        print('cannot remove ' + ip)
        print('you can create a TRUSTFILE by adding IPs to it')


def printUsage():
    print('Incorrect Usage!')
    print('Usage:')
    print('# add ip to domain')
    print('$ python3 trust.py add [ip] [domain]\n')
    print('# remove ip from domain')
    print('$ python3 trust.py remove [ip] [domain]\n')


if __name__ == "__main__":
    import sys
    from banner import banner
    banner()
    if (len(sys.argv) >= 3):
        if (len(sys.argv) == 4 and sys.argv[1] == 'add'):
            add(sys.argv[2], sys.argv[3])
        elif (len(sys.argv) == 4 and sys.argv[1] == 'remove'):
            remove(sys.argv[2], sys.argv[3])
        else:
            printUsage()
    else:
        printUsage()
