from typing import Optional, List, Union, Iterator, Iterable, IO
from copy import deepcopy

from gpx_lite.gpxtrack import GPXTrack


class GPX:
    """
    Container for GPXTracks. This class represents the root element of gpx file.
    All constructor arguments are optional.

    Attributes:
        version: version of gpx schema
        creator: application that created the gpx
        tracks: list of tracks in this gpx
    """

    __slots__ = ('_version', '_creator', '_tracks')

    def __init__(self, version: Optional[str]=None,
                 creator: Optional[str]=None,
                 tracks: Optional[List[GPXTrack]]=None):
        """
        :param version: version of gpx schema
        :param creator: application that created the data
        :param tracks: list of tracks
        """
        self._version: Optional[str] = version
        self._creator: Optional[str] = creator
        self._tracks: List[GPXTrack] = tracks if tracks else []

    def __repr__(self)->str:
        return '<GPX [..%s tracks..]>' % len(self._tracks)

    def __getitem__(self, key: Union[int, slice])-> \
            Union[GPXTrack, List[GPXTrack]]:

        if isinstance(key, int):
            return self._tracks[key]
        elif isinstance(key, slice):
            return self._tracks[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.
                            format(type(key).__name__))

    def __len__(self)->int:
        return len(self._tracks)

    def __contains__(self, item: GPXTrack)->bool:
        return item in self._tracks

    def __iter__(self)->Iterator[GPXTrack]:
        return iter(self._tracks)

    @property
    def tracks(self)->List[GPXTrack]:
        return self._tracks

    @tracks.setter
    def tracks(self, items: List[GPXTrack]):
        self._tracks = items

    @property
    def version(self)->str:
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = version

    @property
    def creator(self)->str:
        return self._creator

    @creator.setter
    def creator(self, creator: str):
        self._creator = creator

    def append(self, item: GPXTrack):
        self._tracks.append(item)

    def extend(self, items:Iterable[GPXTrack]):
        self._tracks.extend(items)

    def remove(self, item: GPXTrack):
        self._tracks.remove(item)

    def to_xml(self, fh: IO)->None:
        version: str = self.version if self.version else '1.1'
        creator: str = self.creator if self.creator else 'gpx-lite.py'
        version_ns: str = version.replace('.', '/')
        result: List[str] = ['<?xml version="1.0" encoding="UTF-8"?>',
                             '\n<gpx xmlns="http://www.topografix.com/GPX/%s" ' % version_ns,
                             'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ',
                             'xsi:schemaLocation="http://www.topografix.com/GPX/%s ' % version_ns,
                             'http://www.topografix.com/GPX/%s/gpx.xsd" ' % version_ns,
                             'version="%s" ' % version,
                             'creator="%s">' % creator]
        for string in result:
            fh.write(string)

        for track in self._tracks:
            track.to_xml(fh)
        fh.write('\n</gpx>')

    def clone(self)->'GPX':
        return deepcopy(self)


if __name__ == '__main__':

    from gpx_lite.gpxtrackpoint import GPXTrackPoint as TrackPoint
    from gpx_lite.gpxtracksegment import GPXTrackSegment as TrackSegment

    x = 50.0164596
    y = 14.4547907
    p1 = TrackPoint(x, y, '2017-11-22T11:03:36Z')
    p2 = TrackPoint(y, x,'2017-11-22T08:03:36Z')
    p3 = TrackPoint(y,y, '2017-11-13T05:11:09Z')
    p4 = TrackPoint(x, x, '2017-11-22T09:03:36Z')
    seg1 = TrackSegment([p1, p2, p3])
    seg2 = TrackSegment([p2, p3, p4])
    seg3 = TrackSegment([p4, p1])
    track1 = GPXTrack('800003627_337', '0', [seg1, seg2, seg3])
    track2 = GPXTrack('800003627_908', None, [seg2, seg3])
    track3 = GPXTrack(None, '2', [TrackSegment([p4])])
    print('Track with name, number, 3 segments: ',track1)
    print('Track with name,no number, 2 segments: ',track2)
    print('Track with no name, number, 1 segment: ', track3)

    gpx = GPX('1.0','gpx.py -- https://github.com/tkrajina/gpxpy')
    print('Empty gpx with version and creator: ', gpx)
    gpx.append(track1)
    print('1 track added: ', gpx)
    gpx.extend([track2,track3])
    print('2 more tracks added, len = ', gpx)

    print('Slice: ', gpx[0:1])
    print('third track: ', gpx[2])

    print('Iterator')
    for t in gpx:
        print(t)

    gpx.remove(track3)
    print('.tracks after 1 track removed: ', gpx.tracks)


