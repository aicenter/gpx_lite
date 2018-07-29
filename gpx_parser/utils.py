from datetime import datetime
from typing import Callable
from re import sub
import xml.etree.ElementTree as ET


def parse_time(string:str, parser:Callable = datetime.strptime)->datetime:
    DATE_FORMATS = [ "%Y-%m-%dT%H:%M:%S.%fZ", '%Y-%m-%dT%H:%M:%SZ']
    for time_format in DATE_FORMATS:
        try:
            return parser(string, time_format)
        except ValueError:
            pass
    raise ValueError('Invalid time format in string %s' % string)


def load_xml(xml_string:str, parser:Callable=ET.fromstring) ->ET.ElementTree:
    """
    :param xml_string: xml represented as a single string
    :return: ElementTree
    """
    xml_string = sub(r'\sxmlns="[^"]+"', '', xml_string , count=1)
    root = parser(xml_string)
    return root




if __name__ == '__main__':

    fn = '/home/olga/Documents/GPX/load_test/traces10.gpx'
    with open(fn, 'r') as xml_file:
        root = load_xml(xml_file.read())
        print(root)



