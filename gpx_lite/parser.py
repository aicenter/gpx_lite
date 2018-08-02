from typing import IO, Callable, List, Dict
from xml.etree.ElementTree import ElementTree, iterparse
from os import fstat
from tqdm import tqdm

from gpx_lite.gpx import GPX, GPXTrack
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
        Parser for relatively small gpx files.
        By default uses xml.etree.ElementTree.fromstring() method
        inside helper function, that also removes namespace from the root tag.

        :param xml_parser: function returning ElementTree with tags that don't contain namespace
        :return: gpx with loaded data
        """
        xml: ElementTree = xml_parser(self._source.read())
        for trk in xml.iterfind('trk'):
                new_track: GPXTrack = GPXTrack()
                try:
                    new_track.name = trk.find('name').text
                except AttributeError:
                    pass
                try:
                    new_track.number = trk.find('number').text
                except AttributeError:
                    pass
                for seg in trk.iterfind('trkseg'):
                    new_segment: GPXTrackSegment = GPXTrackSegment()
                    for point in seg.iterfind('trkpt'):
                        values: Dict[str, str] = point.attrib
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
        """
        Incremental reading for large gpx files using xml.etree.ElementTree.iterparse().
        Loads data from filehandler to gpx object.

        :return: gpx with loaded data
        """
        points: List[GPXTrackPoint] = []
        segments: List[GPXTrackSegment]= []
        tracks: List[GPXTrack] = []
        name: str = ''
        number: str = ''
        time: str = ''
        file_size = fstat(self._source.fileno()).st_size
        with tqdm(total=file_size, unit_scale=True, unit='b', desc="Loading gpx") as pbar:
            for _, elem in iterparse(self._source):
                if 'name' in elem.tag:
                    name = elem.text
                elif 'number' in elem.tag:
                    number = elem.text
                elif 'time' in elem.tag:
                    time = elem.text
                elif 'trkpt' in elem.tag:
                    points.append(GPXTrackPoint(float(elem.attrib['lat']),
                                                float(elem.attrib['lon']),
                                                time))
                elif 'trkseg' in elem.tag:
                    segments.append(GPXTrackSegment([p for p in points]))
                    points.clear()
                elif 'trk' in elem.tag:
                    tracks.append(GPXTrack(name, number, [s for s in segments]))
                    segments.clear()
                elem.clear()
                pbar.update(52)
            self._gpx = GPX(tracks=tracks)
        return self._gpx


if __name__ == '__main__':
    from time import process_time
    fn1 = '/home/olga/Documents/GPX/load_test/traces350.gpx' # 360 Mb
    fn2 = '/home/olga/Documents/GPX/traces-raw.gpx'          # 1.3 Gb
    fn3 = '/home/olga/Documents/GPX/liftago.gpx'             # 3.2 Gb
    # with open(fn1, 'r') as xml_file:
    #     parser = GPXParser(xml_file)
    #     gpx = parser.parse()
    # print(gpx)
    # for track in gpx:
    #     print(track)
    #     for seg in track:
    #         print(seg)
    #         for pt in seg:
    #             print(pt)
    #             print(pt.latitude, pt.longitude,pt.time)

    start = process_time()

    with open(fn3, 'r') as fh:
        parser = GPXParser(fh)
        gpx = parser.iterparse()
    np = sum(map(lambda tr: len(tr[0]), gpx))
    print('Load gpx, %s points at %.2f sec' % (np, process_time() - start))
    #              ,
    # with open('/home/olga/Documents/GPX/save_raw.gpx', 'w') as fh2:
    #     print('Handler ', type(fh2))
    #     gpx.write_to_file(fh2)
    # print(process_time()-start)
    # print(gpx)
