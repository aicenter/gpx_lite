name='gpx_lite'
from typing import IO


__all__ = ['GPX', 'GPXTrack', 'GPXTrackSegment', 'GPXTrackPoint']

from . import GPX


def parse(xml_or_file)->GPX:

    """
    Wrapper fo GPXParser.parse() method.


    :param xml_or_file: xml string or file handler
    :return: gpx loaded from xml
    """
    from . import parser

    parser = parser.GPXParser(xml_or_file)
    return parser.parse()

def iterparse(io_stream:IO)->GPX:
    from . import iterparser

    parser = iterparser.GPXIterparser(io_stream)
    return parser.parse()