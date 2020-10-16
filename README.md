# dmarc-report-analysis
## Warning
This prgram uses an XML parser (Minidom) that creates DOM objects. Minidom is one of the safer libraries but still vulnerable to some attacks. Malicious XML may be able to steal data, crash python or even your machine. Using a Docker container is recommended to prevent damages to your system.
### Useful References:
- https://docs.python.org/3/library/xml.html#xml-vulnerabilities
- https://www.netsparker.com/blog/web-security/xxe-xml-external-entity-attacks/
## add.py
### About
add.py helps with adding new data from a varienty of sources to the buffer. The package inx contains all input sources.
### Requirements
- Python2.7 or later (python 3 recommended)
- scripts
    - in_gmail.py
### Usage
```bash
# bash

$ python3 get.py [input type]
# input types: gmail
```
## query.py
### About
query.py filters records by query. The package outx contains all output methods.
### Requirements
- Python2.7 or later (python 3 recommended)
- scripts
    - out_cli.py
    - out_gmail.py
### Usage
```bash
# bash

$ python3 query.py [output type] [optional: query, query...]
# output types: cli, gmail
# query syntax: key=value
```
## rua_parser.py
### About
rua_parser.py takes XML as input and outputs a list of dictionaries.
### Requirements
- Python2.7 or later (python 3 recommended)
### Usage
```python
# python

# import "rua_parser.py" from package "parser"
from parser import rua_parser

# parse XML-String
parsed = rua_parser.parse('<feedback>...<feedback>')
```
or
```bash
# bash

$ python3 rua_parser.py ["<feedback>...<feedback>"]
```
## gmail_service.py
### About
gmail_service.py builds a Gmail API Service Object and returns it to be used in another Gmail API script.
### Requirements
- Python2.7 or later (python 3 recommended)
- pip
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib
- credentials.json file from Gmail API
```bash
# bash

# run the following command to quickly install the google libraries
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### Helpful Resources
- Python Gmail API Quickstart: https://developers.google.com/gmail/api/quickstart/python
- Gmail API: https://console.developers.google.com/apis/library/gmail.googleapis.com?q=gmail
### Usage
```python
# python

# import service builder
from services import gmail_service

# build service object
service = gmail_service.buildService()
```
## in_gmail.py
### About
in_gmail.py fetches email attachments from the inbox and makes them readable.
### Requirements
- Python 2.7 or later (python 3 recommended)
- scripts
    - gmail_service.py
### Usage
```python
# python

# import gmail input
from inx import in_gmail

# get dictionary of files and contents
filesContents = in_gmail.get()
```
## out_cli.py
### About
out_cli.py "pretty prints" lists of dictionaries containing DMARC record data.
### Requirements
- Python 2.7 or later (python 3 recommended)
### Usage
```python
# python

# import cli output
from outx import out_cli

# build service object
out_cli.printOut(records)
```
## out_gmail.py
### About
out_gmail.py sends HTML versions of lists of dictionaries containing DMARC record data.
### Requirements
- Python 2.7 or later (python 3 recommended)
- scripts
    - gmail_service.py
### Usage
```python
# python

# import gmail output
from outx import out_gmail

# build service object
out_gmail.send(records)
```
