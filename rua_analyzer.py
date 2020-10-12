import sys
from xml.dom import minidom
import trust
import traceback


def analyze(xml):
    dom = minidom.parseString(xml)
    policyPublished = dom.getElementsByTagName('policy_published')[0]
    rootDomain = policyPublished.getElementsByTagName('domain')[
        0].firstChild.data
    rootPolicy = policyPublished.getElementsByTagName('p')[
        0].firstChild.data
    subdomainPolicy = policyPublished.getElementsByTagName('sp')[
        0].firstChild.data
    records = dom.getElementsByTagName('record')
    analysis = []
    TrustChecker = trust.TrustChecker()

    try:
        for record in records:
            auth_results = record.getElementsByTagName('auth_results')[0]

            source_ip = record.getElementsByTagName(
                'source_ip')[0].firstChild.data
            header_from = record.getElementsByTagName(
                'header_from')[0].firstChild.data

            trusted = TrustChecker.getIsTrusted(header_from, source_ip)

            if (len(auth_results.getElementsByTagName('dkim')) >= 1):
                dkim_passed = auth_results.getElementsByTagName(
                    'dkim')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'
            else:
                dkim_passed = 'not found'
            if (len(auth_results.getElementsByTagName('spf')) >= 1):
                spf_passed = auth_results.getElementsByTagName(
                    'spf')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'
            else:
                dkim_passed = 'not found'

            category = None
            if (trusted):
                if (not dkim_passed or not spf_passed):
                    category = 'misconfiguration'
                else:
                    category = 'ok'
            else:
                category = 'fraud'

            analysis.append({
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

    return analysis


def printUsage():
    print('Incorrect Usage!')
    print('Usage: python3 rua_analyzer.py ["<feedback>...</feedback>"]')


if __name__ == "__main__":
    from banner import banner
    banner()
    if (len(sys.argv) == 2):
        analyze(sys.argv[1])
    else:
        printUsage()
