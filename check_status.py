import argparse
from html.parser import HTMLParser
from lxml import html, etree
import requests
from requests.exceptions import HTTPError, ConnectionError
import sys


def list_not_ok_service(host):
    """
    Prints out a list of services with not OK status
    """
    url = 'http://%s' % host
    try:
        r = requests.get(url)
    except (ConnectionError, HTTPError):
        raise
    else:
        if r.status_code != 200:
            sys.exit(-1)
        else:
            doc = html.document_fromstring(r.text)
            for d in etree.XPath("//text()")(doc):
                service_status = d.split()
                if service_status[1] != 'OK':
                    print(f"The service {service_status[0][:-1]} is {' '.join(service_status[1:])}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check status of services')
    parser.add_argument("-a", "--address", help='Hostname to connect to', type=str, dest='host')
    args = parser.parse_args()

    if not args.host:
        print('-a,--address paramter is required')
        print()
        parser.print_help()
        sys.exit(-1)

    try:
        list_not_ok_service(args.host)
    except (ConnectionError, HTTPError):
        sys.exit(-1)
