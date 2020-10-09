# dmarc-report-analysis-and-trust-network
## About
These scripts work together to detect mail server misconfigurations and fraud attempts based on DMARC reports.
## Warning
Carefully crafted XML may be able to break this program or help a hacker perform malicous actions. To prevent damages to the system I recommend running these scripts inside a docker container.
[Official Python Docker Container >](https://hub.docker.com/_/python/)
## rua_analyser.py
### About
rua_analyser.py takes an XML string as an input, either from the command line or as a parameter in python. This input is parsed and a summary of each record within is returned as a Python list of dictionaries. 
The output will look something like this:
```bash
[
    {
        'source_ip': 1.2.3.4,
        'header_from': 'example.com',
        'trusted': True,
        'dkim_passed': True,
        'spf_passed': False,
        'policy': 'reject'
    },
    {
        'source_ip': 4.3.2.1,
        'header_from': 'example.com',
        'trusted': False,
        'dkim_passed': False,
        'spf_passed': False,
        'policy': 'none'
    },
    .
    .
    .
]
```
### Requirements
- Python2.7 or later (python 3 recommended)
### Usage
```python
# python

# import analyser
from rua_analyser import analyse

# analyse xml string
result = analyse("<feedback>...</feedback>")
```
or
```bash
# bash

$ python3 rua_analyser.py ["<feedback>...</feedback>"]
```
## trust.py
### About
trust.py manages which ips are allowed/trusted to send emails from a certain domain. The script itself can add and remove trusted ips from domains and search for ips and domains.
### Requirements
- Python2.7 or later (python 3 recommended)
### Usage
```python
# python

# import trust
import trust

# create new trust and trustfile handle
TrustChecker = trust.TrustChecker()

# verify if source_ip is trusted to access email for domain
isTrusted = TrustChecker.getIsTrusted('example.com', '1.2.3.4')

# close trustfile handle
TrustChecker.close()
```
or
```bash
# bash

# add ip to domain
$ python3 trust.py add [ip] [domain]
# search for ip or domain
$ python3 trust.py search [ip or domain]
# remove ip from domain
$ python3 trust.py remove [ip] [domain]
```
## cli.py
### About
cli.py is a better way to use rua_analyser.py from the command line. 
### Requirements
- Python2.7 or later (python 3 recommended)
### Usage
```bash
# bash

$ python3 cli.py [filepath]
```
## io_handler_gmail.py
### About
io_handler_gmail.py uses the gmail API to autonomously get DMARC reports and send reports listing all the fails.
### Requirements
- Python2.7 or later (python 3 recommended)
- Google Mail account
- credentials.json file from Gmail API
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
### Helpful Resources
- Python Gmail API Quickstart: https://developers.google.com/gmail/api/quickstart/python
- Gmail API: https://console.developers.google.com/apis/library/gmail.googleapis.com?q=gmail
### Usage
```bash
# bash

# get new reports from inbox
$ python3 io_handler_gmail.py get
# send all collected report data and reset
$ python3 io_handler_gmail.py report
```
