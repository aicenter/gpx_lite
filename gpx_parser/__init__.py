name='gpx_lite'

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
