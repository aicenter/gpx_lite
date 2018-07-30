from datetime import datetime
from typing import Callable
from re import sub
import xml.etree.ElementTree as ET


def parse_time(string: str, parser: Callable = datetime.strptime)->datetime:
    """

    :param string: date and time as a string
    :param parser: function to convert string to datetime
    :return: datetime.datetime
    """
    date_formats = ["%Y-%m-%dT%H:%M:%S.%fZ",
                    '%Y-%m-%dT%H:%M:%SZ']
    for df in date_formats:
        try:
            return parser(string, df)
        except ValueError:
            pass
    raise ValueError('Invalid time format in string %s' % string)


def parse_xml(xml_string: str, parser: Callable=ET.fromstring)->ET.ElementTree:
    """
    Helper function to read xml Element Tree from string.
    
    :param xml_string: xml represented as a single string
    :param parser: function to read xml from string
    :return: ElementTree
    """
    #remove namespace from the root of gpx, so it won't appear in tags.
    xml_string = sub(r'\sxmlns="[^"]+"', '', xml_string , count=1)
    return parser(xml_string)



if __name__ == '__main__':

    fn = '/home/olga/Documents/GPX/load_test/traces10.gpx'
    with open(fn, 'r') as xml_file:
        root = parse_xml(xml_file.read())
        print(root)



