#!/usr/bin/python3

# This is just a pretty litte banner.

# Usage:
#  python
#    from banner import banner
#    banner()
#  bash
#    python3 banner.py

def banner():
    print('\n'.join([
        ' ____  __  __    _    ____   ____ ',
        '|  _ \\|  \\/  |  / \\  |  _ \\ / ___|',
        '| | | | |\\/| | / _ \\ | |_) | |    ',
        '| |_| | |  | |/ ___ \\|  _ <| |___ ',
        '|____/|_|  |_/_/   \\_\\_| \\_\\\\____|',
        'Domain-based Message Authentication,\nReporting and Conformance\n'
    ]))


if __name__ == "__main__":
    banner()
