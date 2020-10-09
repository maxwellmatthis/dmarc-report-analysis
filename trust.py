import os
import json
import re

trustfile = 'trust.json'

ipv4Pattern = re.compile(
    r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.25[0-5]|\.2[0-4][0-9]|\.[01]?[0-9][0-9]?){3})')
ipv6Pattern = re.compile(
    r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))')
domainPattern = re.compile(
    r'[0-9a-zA-Z]+\.[0-9a-zA-Z]{2,}')


class TrustChecker:
    def __init__(self):
        if (not os.path.isfile(trustfile)):
            open(trustfile, 'w').write('{}')
        self.trustFileHandle = open(trustfile, 'r')
        self.trust = json.load(self.trustFileHandle)

    def getIsTrusted(self, domain, ip):
        if (domain in self.trust and
            type(self.trust[str(domain)]) is list and
                ip in self.trust[domain]):
            return True
        else:
            return False

    def close(self):
        self.trustFileHandle.close()


def add(ip, domain):
    if (not os.path.isfile(trustfile)):
        open(trustfile, 'w').write('{}')
        print('created trustfile')

    contents = json.load(open(trustfile, 'r'))
    if (domain in contents and type(contents[domain]) is list):
        if (not ip in contents[domain]):
            contents[domain].append(ip)
            print('added ' + ip + ' to ' + domain)
        else:
            print(ip + ' is already trusted on ' + domain)
    else:
        contents[domain] = [ip]
        print('added ' + ip + ' to ' + domain)

    trustFileHandle = open(trustfile, 'w')
    json.dump(contents, trustFileHandle)
    trustFileHandle.close()


def search(string):
    _type = None
    if ((ipv4Pattern.search(string) is not None and ipv4Pattern.search(string).groups()[0] == string) or (ipv6Pattern.search(string) is not None and ipv6Pattern.search(string).groups()[0] == string)):
        _type = 'ip'
    elif (domainPattern.search(string).groups()[0] == string):
        _type = 'domain'
    else:
        print(string + ' is not a valid ipv4 or ipv6 ip or domain')
        return
    print('searching for ' + _type + ' ' + string + '...\n')

    if (os.path.isfile(trustfile)):
        contents = json.load(open(trustfile, 'r'))
        if (_type == 'ip'):
            occurrences = []
            for key in contents:
                if (string in contents[key]):
                    occurrences.append(key)
            if (len(occurrences) >= 1):
                print(string + ' is trusted on:')
                for domain in occurrences:
                    print(domain)
            else:
                print(string + ' is not trusted on anything')

        if (_type == 'domain'):
            if (string in contents):
                print(string + '')
            else:
                print(string + ' does not have any trusted hosts')
    else:
        print('ERROR: no trustfile')
        print('cannot find ' + _type + ' ' + string)
        print('you can create a trustfile by adding IPs to it')


def remove(ip, domain):
    if (os.path.isfile(trustfile)):
        contents = json.load(open(trustfile, 'r'))
        if (domain in contents and type(contents[domain]) is list):
            if (not ip in contents[domain]):
                contents[domain].remove(ip)
                print('removed ' + ip + ' from ' + domain)
            else:
                print(ip + ' wasn\'t not trusted on ' + domain)
        else:
            print(domain + ' doesn\'t have any trusted ips')

        trustFileHandle = open(trustfile, 'w')
        json.dump(contents, trustFileHandle)
        trustFileHandle.close()

    else:
        print('ERROR: no trustfile')
        print('cannot remove ' + ip)
        print('you can create a trustfile by adding IPs to it')


def printUsage():
    print('Incorrect Usage!')
    print('Usage:')
    print('# add ip to domain')
    print('$ python3 trust.py add [ip] [domain]\n')
    print('# search for ip or domain')
    print('$ python3 trust.py search [ip or domain]\n')
    print('# remove ip from domain')
    print('$ python3 trust.py remove [ip] [domain]\n')


if __name__ == "__main__":
    import sys
    from banner import banner
    banner()
    if (len(sys.argv) >= 3):
        if (len(sys.argv) == 4 and sys.argv[1] == 'add'):
            add(sys.argv[2], sys.argv[3])
        elif (len(sys.argv) == 3 and sys.argv[1] == 'search'):
            search(sys.argv[2])
        elif (len(sys.argv) == 4 and sys.argv[1] == 'remove'):
            remove(sys.argv[2], sys.argv[3])
        else:
            printUsage()
    else:
        printUsage()
