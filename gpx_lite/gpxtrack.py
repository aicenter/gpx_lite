from typing import Union, Optional, List, Iterator, Iterable
from copy import deepcopy

from gpx_lite.gpxtrackpoint import GPXTrackPoint
from gpx_lite.gpxtracksegment import GPXTrackSegment


class GPXTrack:
    """
    Attributes:
        name:  track name, str or None
        number:  track number, int or None
        segments:  list of GPXTrackSegments
    """

    __slots__ = ('_name', '_number', '_segments')

    def __init__(self, name: Optional[str]=None,
                 number: Optional[str]=None,
                 segments: Optional[List[GPXTrackSegment]]=None):
        self._name: Optional[str] = name
        self._number: Optional[int] = int(number) if number else None
        self._segments: List[GPXTrackSegment] = segments if segments else []

    def __repr__(self)->str:
        return '<GPXTrack %s %s [.%s segments.]>' \
               % (self._name, self._number, len(self._segments))

    def __len__(self)->int:
        return len(self._segments)

    def __iter__(self)->Iterator[GPXTrackSegment]:
        return iter(self._segments)

    def __getitem__(self, key: int)->Union[GPXTrackSegment,
                                           List[GPXTrackSegment]]:
        if isinstance(key, int):
            return self._segments[key]
        elif isinstance(key,slice):
            return self._segments[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.
                            format(type(key).__name__))

    def __contains__(self, item: GPXTrackSegment)->bool:
        return item in self._segments

    @property
    def name(self)->str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def number(self)->int:
        return self._number

    @number.setter
    def number(self, num: str):
        self._number = int(num)

    @property
    def segments(self)->List[GPXTrackSegment]:
        return self._segments

    @segments.setter
    def segments(self, segments: List[GPXTrackSegment])->None:
        self._segments = segments

    @property
    def points(self)->List[GPXTrackPoint]:
        """

        :return: list of all points from all the segments
        """
        return [pt for seg in self._segments for pt in seg.points]

    def get_points_no(self)->int:
        """

        :return: total number of points in all segments
        """
        return sum(map(lambda seg: len(seg), self._segments))

    def append(self, item: GPXTrackSegment):
        self._segments.append(item)

    def extend(self, items: Iterable[GPXTrackSegment]):
        self._segments.extend(items)

    def remove(self,item: GPXTrackSegment):
        self._segments.remove(item)

    def remove_empty(self)->None:
        """
        Removes empty segmets from the track
        :return:
        """
        self._segments = [seg for seg in filter(
            lambda seg: len(seg) > 0, self._segments)]

    def to_xml(self)->str:
        """
        :return: track as xml string
        """
        result:List[str] = ['\n<trk>',]
        if self._name:
            result.extend(['\n<name>',self._name,'</name>'])
        if self._number is not None:
            result.extend(['\n<number>', str(self._number), '</number>'])
        result.extend(map(lambda seg: seg.to_xml(), self._segments))
        result += '\n</trk>'
        return ''.join(result)

    def clone(self)->'GPXTrack':
        return deepcopy(self)


if __name__ == '__main__':

    from gpx_lite.gpxtrackpoint import GPXTrackPoint as TrackPoint

    x = 50.0164596
    y = 14.4547907
    p1 = TrackPoint(x, y, '2017-11-22T11:03:36Z')
    p2 = TrackPoint(y, x,'2017-11-22T08:03:36Z')
    p3 = TrackPoint(y,y, '2017-11-13T05:11:09Z')
    p4 = TrackPoint(x, x, '2017-11-22T09:03:36Z')
    seg1 = GPXTrackSegment([p1, p2, p3])
    seg2 = GPXTrackSegment([p2, p3, p4])
    track = GPXTrack('800003627_337', '0')
    print('Empty track with name and number: ', track)
    track.append(seg1)
    print('1 segment added, len = ',  len(track))
    seg3 = GPXTrackSegment([p4, p1])
    track.extend([seg2, seg3])
    print('2 more segments added, len: ', len(track))
    print('Points in all segments: ', track.get_points_no())
    print('Slice: ', track[2:])
    print('Iterator')
    for s in track:
        print(s)

    track.remove(seg1)
    print('1 segment removed: ', len(track))
