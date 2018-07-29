name='gpx_lite'
from typing import IO
from . import GPX

__all__ = ['GPX', 'GPXTrack', 'GPXTrackSegment', 'GPXTrackPoint']


def parse(file:IO)->GPX:

    """
    Wrapper fo GPXParser.parse()  and
    GPXParser.parse() methods.

    :param file: file handler
    :return: gpx loaded from xml
    """
    from . import parser
    parser= parser.GPXParser(file)
    return parser.parse()

def iterparse(file:IO)->GPX:
    from . import parser

    parser = parser.GPXParser(file)
    return parser.iterparse()