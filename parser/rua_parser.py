import sys
from xml.dom import minidom
import traceback

def parse(xml):
    # aggregated report xml
    dom = minidom.parseString(xml)

    # report
    policy_published = dom.getElementsByTagName('policy_published')[0]
    ## root domain
    rootDomain = policy_published.getElementsByTagName('domain')[0].firstChild.data
    ## policy
    root_policy = policy_published.getElementsByTagName('p')[0].firstChild.data
    subdomain_policies = policy_published.getElementsByTagName('sp')
    if (len(subdomain_policies) >= 1 and hasattr(subdomain_policies[0], 'firstChild') and hasattr(subdomain_policies[0].firstChild, 'data')):
        subdomain_policy = subdomain_policies[0].firstChild.data
    else: subdomain_policy = 'not found'

    # records
    records = dom.getElementsByTagName('record')

    parsed = []

    try:
        for record in records:
            # ip
            source_ip = record.getElementsByTagName('source_ip')[0].firstChild.data

            # policy
            policy_evaluated = record.getElementsByTagName('policy_evaluated')[0]
            ## dkim
            if (len(policy_evaluated.getElementsByTagName('dkim')) >= 1): dkim_evaluated = policy_evaluated.getElementsByTagName('dkim')[0].firstChild.data == 'pass'
            else: dkim_evaluated = 'not found'
            ## spf
            if (len(policy_evaluated.getElementsByTagName('spf')) >= 1): spf_evaluated = policy_evaluated.getElementsByTagName('spf')[0].firstChild.data == 'pass'
            else: spf_evaluated = 'not found'
            
            # identifiers
            header_from = record.getElementsByTagName('header_from')[0].firstChild.data

            # auth
            auth_results = record.getElementsByTagName('auth_results')[0]
            ## dkim
            if (len(auth_results.getElementsByTagName('dkim')) >= 1): dkim_passed = auth_results.getElementsByTagName('dkim')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'
            else: dkim_passed = 'not found'
            ## dkim domain
            if (len(auth_results.getElementsByTagName('dkim')) >= 1): dkim_domain = auth_results.getElementsByTagName('dkim')[0].getElementsByTagName('domain')[0].firstChild.data
            else: dkim_domain = 'not found'
            ## spf
            if (len(auth_results.getElementsByTagName('spf')) >= 1): spf_passed = auth_results.getElementsByTagName('spf')[0].getElementsByTagName('result')[0].firstChild.data == 'pass'
            else: spf_passed = 'not found'
            ## spf domain
            if (len(auth_results.getElementsByTagName('spf')) >= 1): spf_domain = auth_results.getElementsByTagName('spf')[0].getElementsByTagName('domain')[0].firstChild.data
            else: spf_domain = 'not found'

            parsed.append({
                # dmarc report policy
                'policy': root_policy if (header_from == rootDomain) else subdomain_policy,

                # ip
                'source_ip': source_ip,

                # policy
                'dkim_evaluated': dkim_evaluated,
                'spf_evaluated': spf_evaluated,

                # identifiers
                'header_from': header_from,

                # auth
                'dkim_passed': dkim_passed,
                'dkim_domain': dkim_domain,
                'spf_passed': spf_passed,
                'spf_domain': spf_domain,
            })
    except:
        traceback.print_exception(*sys.exc_info())

    return parsed

def printUsage():
    print('Incorrect Usage!')
    print('Usage: python3 rua_parser.py ["<feedback>...</feedback>"]')

if __name__ == "__main__":
    if (len(sys.argv) == 2):
        print(parse(sys.argv[1]))
    else:
        printUsage()
