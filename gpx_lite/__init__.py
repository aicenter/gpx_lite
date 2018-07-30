from typing import IO
from .gpx import GPX


name = ' gpx_lite '
__all__ = ['gpx.py', 'gpxtrack.py', 'gpxtracksegment.py', 'gpxtrackpoint.py']


def parse(file: IO)->GPX:

    """
    Wrapper fo GPXParser.parse(),
    loads gpx from xml file.

    :param file: file handler
    :return: gpx loaded from xml
    """
    from . import parser

    parser = parser.GPXParser(file)
    return parser.parse()


def iterparse(file: IO)->GPX:

    """
    Wrapper fo GPXParser.iterparse(),
    loads gpx from xml file.

    :param file: file handler
    :return: gpx loaded from xml
    """

    from . import parser

    parser = parser.GPXParser(file)
    return parser.iterparse()