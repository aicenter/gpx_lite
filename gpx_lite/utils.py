from datetime import datetime
from typing import Callable, List
from re import sub
import xml.etree.ElementTree as ET


def parse_time(string: str, parser: Callable = datetime.strptime)->datetime:
    """
    :param string: date and time as a string
    :param parser: function to convert string to datetime
    :return: datetime.datetime
    """
    date_formats: List[str] = ["%Y-%m-%dT%H:%M:%S.%fZ",
                    '%Y-%m-%dT%H:%M:%SZ']
    for df in date_formats:
        try:
            return parser(string, df)
        except ValueError:
            pass
    raise ValueError('Invalid time format in string %s' % string)


def parse_xml(xml_string: str, parser: Callable=ET.fromstring)->ET.ElementTree:
    """
    Helper function to remove namespace and read ElementTree from string.
    
    :param xml_string: xml represented as a single string
    :param parser: function to read xml from string
    :return: ElementTree
    """
    xml_string = sub(r'\sxmlns="[^"]+"', '', xml_string, count=1) #otherwise ns will appear in tags
    return parser(xml_string)


def time_to_int(time: str) -> int:
    if len(time) == 24:
        time = time[:4] + time[5:7] + time[8:10] \
               + time[11:13] + time[14:16] + time[17:19] + time[20:23]
       # print(time)
    else:
        time = time[:4] + time[5:7] + time[8:10] \
               + time[11:13] + time[14:16] + time[17:19]
        #print(time)
    return int(time)


def time_to_str(time: float) -> str:
    time: str = str(time)
    if len(time) == 17:
        time = time[:4] + '-' + time[4:6] + '-' + time[6:8] \
               + 'T' + time[8:10] + ':' + time[10:12] + ':' + time[12:14] \
               + '.' + time[14:] + 'Z'
        #print(time)
    else:
        time = time[:4] + '-' + time[4:6] + '-' + time[6:8] \
               + 'T' + time[8:10] + ':' + time[10:12] + ':' + time[12:14] \
               + 'Z' + time[14:]
        #print(time)

    return time


if __name__ == '__main__':
    fn = '/home/olga/Documents/GPX/load_test/traces10.gpx'
    with open(fn, 'r') as xml_file:
        root = parse_xml(xml_file.read())
        print(root)



