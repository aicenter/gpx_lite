from typing import IO, Callable, List
from xml.etree.ElementTree import ElementTree, iterparse

from gpx_lite.gpx import GPX
from gpx_lite.gpxtrack import GPXTrack
from gpx_lite.gpxtrackpoint import GPXTrackPoint
from gpx_lite.gpxtracksegment import GPXTrackSegment
from gpx_lite.utils import parse_xml


class GPXParser:
    """
    Parser for gpx tracks.

    Args:
       file:  file handler

    Usage:

        import gpx-lite as parser
                 ...
        with open(filename, 'r') as gpx_file:
            gpx:GPX = parser.parse(gpx_file)
                  or
            gpx:GPX = parser.iterparse(gpx_file)

    """

    __slots__ = ('_gpx', '_source')

    def __init__(self, file: IO)->None:
        self._source: IO = file
        self._gpx: GPX = GPX()

    def parse(self, xml_parser: Callable = parse_xml)->GPX:
        """

        :param xml_parser:
        :return:
        """
        xml: ElementTree = xml_parser(self._source.read())
        for trk in xml.iterfind('trk'):
            new_track = GPXTrack()
            try:
                new_track.name = trk.find('name').text
            except AttributeError:
                pass
            try:
                new_track.number = trk.find('number').text
            except AttributeError:
                pass
            for seg in trk.iterfind('trkseg'):
                new_segment = GPXTrackSegment()
                for point in seg.iterfind('trkpt'):
                    values = point.attrib
                    try:
                        point.attrib['time'] = point.find('time').text
                    except AttributeError:
                        point.attrib['time'] = None
                    new_point = GPXTrackPoint(float(values['lat']),
                                              float(values['lon']),
                                              values['time'])
                    new_segment.append(new_point)
                new_track.append(new_segment)
            self._gpx.append(new_track)
        return self._gpx

    def iterparse(self)->GPX:
        points: List[GPXTrackPoint] = []
        segments: List[GPXTrackSegment]= []
        tracks: List[GPXTrack] = []
        name: str = ''
        number: str = ''
        time: str = ''

        for _, elem in iterparse(self._source):
            if 'name' in elem.tag:
                name = elem.text
            elif 'number' in elem.tag:
                number = elem.text
            elif 'time' in elem.tag:
                time = elem.text
            elif 'trkpt' in elem.tag:
                points.append(GPXTrackPoint(float(elem.attrib['lat']),
                                         float(elem.attrib['lon']), time))
            elif 'trkseg' in elem.tag:
                segments.append(GPXTrackSegment([p for p in points]))
                points.clear()
            elif 'trk' in elem.tag:
                tracks.append(GPXTrack(name, number, [s for s in segments]))
                segments.clear()
            elem.clear()
        self._gpx = GPX(tracks=tracks)
        return self._gpx



if __name__ == '__main__':
    fn = '/home/olga/Documents/GPX/test1.gpx'
    with open(fn, 'r') as xml_file:
        parser = GPXParser(xml_file)
        gpx = parser.parse()
    print(gpx)
    for track in gpx:
        print(track)
        for seg in track:
            print(seg)
            for pt in seg:
                print(pt)
                print(pt.latitude, pt.longitude,pt.time)

    fn2 = '/home/olga/Documents/GPX/traces-raw.gpx'
    with open(fn2, 'r') as fh:
        parser = GPXParser(fh)
        gpx = parser.iterparse()
    print(gpx)
