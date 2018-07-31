from typing import Union, Optional, List, Iterator, Iterable, IO
from copy import deepcopy

from gpx_lite.gpxtrackpoint import GPXTrackPoint


class GPXTrackSegment:

    __slots__ = '_points'

    def __init__(self, points: Optional[List[GPXTrackPoint]]=None):
        self._points = points if points else []

    def __repr__(self)-> str:
        return 'GPXTrackSegment(%s)(points=%s)' % \
               (len(self._points), self._points)

    def __len__(self)-> int:
        return len(self._points)

    def __getitem__(self, key:Union[int, slice])-> \
            Union[GPXTrackPoint, List[GPXTrackPoint]]:
        if isinstance(key, int):
            return self.points[key]
        elif isinstance(key, slice):
            return self.points[key.start:key.stop:key.step]
        else:
            raise TypeError('Index must be int, not {}'.
                            format(type(key).__name__))

    def __iter__(self)->Iterator[GPXTrackPoint]:
        return iter(self.points)

    def __contains__(self, item: GPXTrackPoint)->bool:
        return item in self.points

    @property
    def points(self)->List[GPXTrackPoint]:
        return self._points

    @points.setter
    def points(self, points: List[GPXTrackPoint]):
        self._points = points

    def append(self, item: GPXTrackPoint):
        self._points.append(item)

    def extend(self, items: Iterable[GPXTrackPoint]):
        self._points.extend(items)

    def remove(self, item: GPXTrackPoint):
        self._points.remove(item)

    def get_points_no(self)->int:
        """
        Gets the number of points in segment.
        """
        return len(self._points)

    def to_xml(self, fh:IO)->None:
        fh.write('\n<trkseg>')
        for pt in self._points:
            pt.to_xml(fh)
        fh.write('\n</trkseg>')

    def sort_by_time(self)->None:
        self._points.sort(key=lambda pt: pt._time)

    def clone(self):
        return deepcopy(self)


if __name__ == '__main__':

    x = 50.0164596
    y = 14.4547907
    p1 = GPXTrackPoint(x, y, '2017-11-22T07:03:36Z')
    p3 = GPXTrackPoint(y,y, '2617-11-13T08:11:09Z')
    p2 = GPXTrackPoint(x, x, '2017-12-02T07:03:36Z')
    p4 = GPXTrackPoint(y,x, '1717-11-13T08:11:09Z')
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

