from typing import IO, Callable, List
from xml.etree.ElementTree import ElementTree, iterparse

from gpx_parser.gpx import GPX
from gpx_parser.gpxtrack import GPXTrack as Track
from gpx_parser.gpxtrackpoint import GPXTrackPoint as TrackPoint
from gpx_parser.gpxtracksegment import GPXTrackSegment as TrackSegment
from gpx_parser.utils import load_xml


class GPXParser:
    """
    Parser for gpx tracks.

    Args:
       file:  file handler

    Usage:

        import gpx-lite as parser
                 ...
        gpx:GPX = parser.parse(gpx_file)
        gpx:GPX = parser.iterparse(gpx_file)


    """

    __slots__ = ('gpx', 'source')

    def __init__(self, file:IO):
        self.source: IO = file
        self.gpx:GPX = GPX()

    def parse(self, loader:Callable = load_xml) ->GPX:
        xml:ElementTree = loader(self.source.read())
        for track in xml.iterfind('trk'):
            new_track = Track()
            try:
                new_track.name = track.find('name').text
            except AttributeError:
                pass
            try:
                new_track.number = track.find('number').text
            except AttributeError:
                pass
            for segment in track.iterfind('trkseg'):
                new_segment = TrackSegment()
                for point in segment.iterfind('trkpt'):
                    values = point.attrib
                    try:
                        point.attrib['time'] = point.find('time').text
                    except AttributeError:
                        point.attrib['time'] = None
                    new_point = TrackPoint(float(values['lat']), float(values['lon']), values['time'])
                    new_segment.append(new_point)
                new_track.append(new_segment)
            self.gpx.append(new_track)
        return self.gpx

    def iterparse(self) ->GPX:
        points:List[TrackPoint] = []
        segments:List[TrackSegment]= []
        tracks:List[Track] = []
        name:str = ''
        number:str = ''
        time:str = ''

        for _, elem in iterparse(self.source):
            if 'name' in elem.tag:
                name = elem.text
            elif 'number' in elem.tag:
                number = elem.text
            elif 'time' in elem.tag:
                time = elem.text
            elif 'trkpt' in elem.tag:
                points.append(TrackPoint(float(elem.attrib['lat']),
                                         float(elem.attrib['lon']), time))
            elif 'trkseg' in elem.tag:
                segments.append(TrackSegment([p for p in points]))
                points.clear()
            elif 'trk' in elem.tag:
                tracks.append(Track(name, number, [s for s in segments]))
                segments.clear()
            elem.clear()
        self.gpx = GPX(tracks=tracks)
        return self.gpx



if __name__ == '__main__':
    fn = '/home/olga/Documents/GPX/test1.gpx'
    with open(fn, 'r') as xml_file:
        parser = GPXParser(xml_file)
        gpx = parser.parse()
    print(gpx)
    print(len(gpx))
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
