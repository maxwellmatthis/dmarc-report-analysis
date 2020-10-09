import sys
from xml.dom import minidom
import trust
import traceback


def analyse(xml):
    dom = minidom.parseString(xml)
    policyPublished = dom.getElementsByTagName('policy_published')[0]
    rootDomain = policyPublished.getElementsByTagName('domain')[
        0].firstChild.data
    rootPolicy = policyPublished.getElementsByTagName('p')[
        0].firstChild.data
    subdomainPolicy = policyPublished.getElementsByTagName('sp')[
        0].firstChild.data
    records = dom.getElementsByTagName('record')
    analyses = []
    TrustChecker = trust.TrustChecker()

    try:
        for record in records:
            auth_results = record.getElementsByTagName('auth_results')[0]

            source_ip = record.getElementsByTagName(
                'source_ip')[0].firstChild.data
            header_from = record.getElementsByTagName(
                'header_from')[0].firstChild.data

            trusted = TrustChecker.getIsTrusted(header_from, source_ip)

            dkim_passed = auth_results.getElementsByTagName(
                'dkim')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'
            spf_passed = auth_results.getElementsByTagName(
                'spf')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'

            category = None
            if (trusted):
                if (not dkim_passed or not spf_passed):
                    category = 'misconfiguration'
                else:
                    category = 'ok'
            else:
                category = 'fraud'

            analyses.append({
                'source_ip': source_ip,
                'header_from': header_from,
                'trusted': trusted,
                'dkim_passed': dkim_passed,
                'spf_passed': spf_passed,
                'policy': rootPolicy if (
                    header_from == rootDomain) else subdomainPolicy,
                'category': category
            })
    except:
        traceback.print_exception(*sys.exc_info())

    TrustChecker.close()
    return analyses


def printUsage():
    print('Incorrect Usage!')
    print('Usage: python3 rua_analyser.py ["<feedback>...</feedback>"]')


if __name__ == "__main__":
    from banner import banner
    banner()
    if (len(sys.argv) == 2):
        analyse(sys.argv[1])
    else:
        printUsage()
