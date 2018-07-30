from typing import Union, Optional, List, Iterator, Iterable
from copy import deepcopy
from xml.etree import ElementTree as ET
from gpx_parser.gpxtrackpoint import GPXTrackPoint as TrackPoint


class GPXTrackSegment:
    __slots__ = ('_points')

    def __init__(self, points:Optional[List[TrackPoint]]=None):
        self._points = points if points else []

    def __repr__(self)-> str:
        return 'GPXTrackSegment(%s)(points=%s)' % (len(self._points), self._points)

    def __len__(self)-> int:
        return len(self._points)

    def __getitem__(self, key:Union[int, slice])-> Union[TrackPoint, List[TrackPoint]]:
        if isinstance(key, int):
            return  self.points[key]

        elif isinstance(key, slice):
            return self.points[key.start:key.stop:key.step]

        else:
            raise TypeError('Index must be int, not {}'.format(type(key).__name__))


    def __iter__(self)->Iterator[TrackPoint]:
        return iter(self.points)

    def __contains__(self, item:TrackPoint)->bool:
        return item in self.points

    @property
    def points(self)->List[TrackPoint]:
        return self._points

    @points.setter
    def points(self, points:List[TrackPoint]):
        self._points = points

    def append(self, item:TrackPoint):
        self._points.append(item)


    def extend(self, items:Iterable[TrackPoint]):
        self._points.extend(items)

    def remove(self, item:TrackPoint):
        self._points.remove(item)


    def get_points_no(self)->int:
        """
        Gets the number of points in segment.
        """
        return len(self._points)

    def to_xml(self)->str:
        result:List[str] = ['\n<trkseg>',]
        result.extend(map(lambda pt : pt.to_xml(), self._points))
        result.append('\n</trkseg>')
        return ''.join(result)

    def clone(self):
        return deepcopy(self)


if __name__ == '__main__':

    x = 50.0164596
    y =  14.4547907
    p1 = TrackPoint(x, y, '2017-11-22T07:03:36Z')
    p3 = TrackPoint(y,y, '2617-11-13T08:11:09Z')
    p2 = TrackPoint(x, x, '2017-12-02T07:03:36Z')
    p4 = TrackPoint(y,x, '1717-11-13T08:11:09Z')
    seg = GPXTrackSegment()
    print('Empty segment: ', seg)
    seg.append(p1)
    print('Length,  1 point: ', len(seg))
    seg.extend([p2,p3])
    print('0th element: ', seg[0])
    print('Segment with 3 points: ', seg)
    print('seg.points: ', seg.points)

    print('Point in segment: %s, not in segment: %s ' % (
        p1 in seg, p4 in seg))

    print('Slice: ', seg[1:2:2])
    print('Iterator:')
    for p in seg:
        print(p)

