name='gpx_lite'
from gpx_parser.GPX import GPX

__all__ = ['GPX', 'GPXTrack', 'GPXTrackSegment', 'GPXTrackPoint']


def parse(xml_or_file)->GPX:
    """
    Wrapper fo GPXParser.parse() method.

    :param xml_or_file: xml string or file handler
    :return: gpx loaded from xml
    """
    from . import parser

    parser = parser.GPXParser(xml_or_file)
    return parser.parse()
