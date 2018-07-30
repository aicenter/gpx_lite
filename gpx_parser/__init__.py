name='gpx_lite'
from typing import IO
from . import gpx

__all__ = ['gpx.py', 'gpxtrack.py', 'gpxtracksegment.py', 'gpxtrackpoint.py']


def parse(file:IO)->gpx:

    """
    Wrapper fo GPXParser.parse()  and
    GPXParser.parse() methods.

    :param file: file handler
    :return: gpx loaded from xml
    """
    from . import parser
    parser= parser.GPXParser(file)
    return parser.parse()

def iterparse(file:IO)->gpx:
    from . import parser

    parser = parser.GPXParser(file)
    return parser.iterparse()