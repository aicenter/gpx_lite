from xml.etree.ElementTree import ElementTree as ET, Element, iterparse
from typing import Union, Optional, List, Callable, IO


from gpx_parser.GPX import GPX
from gpx_parser.GPXTrackPoint import GPXTrackPoint as TrackPoint
from gpx_parser.GPXTrackSegment import GPXTrackSegment as TrackSegment
from gpx_parser.GPXTrack import GPXTrack as Track



class GPXIterparser:
    """
    Incremental parser for large gpx files.

    Args:
        stream:  io stream with xml file

    Usage:

        import gpx-lite as my_parser
                 ...
        with open(gpx_file, 'r) as io:
            gpx:GPX = my_parser.iterparse(io)

    """

    __slots__ = ('gpx', 'source')

    def __init__(self, stream:IO):
        self.source:IO = stream
        self.gpx:GPX = GPX()

    def parse(self) ->GPX:
        points:List[TrackPoint] = []
        segments:List[TrackSegment]= []
        tracks:List[Track] = []
        name:str = ''
        number:str = ''
        time:str = ''

        for event, elem in iterparse(self.source):
            # print('Event = %s , element = %s' % (event, elem))
            if 'name' in elem.tag:
                name = elem.text
                # print(name)
            elif 'number' in elem.tag:
                number = elem.text
                # print(number)
            elif 'time' in elem.tag:
                time = elem.text
                # print(time)
            elif 'trkpt' in elem.tag:
                # print(elem.attrib)
                points.append(TrackPoint(float(elem.attrib['lat']),
                                         float(elem.attrib['lon']), time))
            elif 'trkseg' in elem.tag:
                segments.append(TrackSegment(points))
                points.clear()
            elif 'trk' in elem.tag:
                # print('TRACK: ', elem)
                tracks.append(Track(name, number, segments))
                segments.clear()
            elem.clear()
        self.gpx = GPX(tracks=tracks)
        return self.gpx



if __name__=='__main__':
    fn = '/home/olga/Documents/GPX/traces-raw.gpx'
    with open(fn, 'r') as io:
        parser = GPXIterparser(io)
        print(parser.parse())
