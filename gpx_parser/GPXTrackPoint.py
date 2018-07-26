from math import cos, pi, sqrt
from datetime import datetime,timedelta
from typing import Optional, Callable, List, Union
from collections import namedtuple
from gpx_parser.utils import parse_time


Point = namedtuple('Point', ['lat', 'lon', 'time'])


class GPXTrackPoint:
    """
    Leaf element of gpx structure.

    Attributes:
        latitude: float
        longitude: float
        time:    datetime or None

    """

    __slots__ = ('_lat', '_lon', '_time')

    def __init__(self, lat:float, lon:float, time:Optional[str]=None)->None:
        self._lat:float = lat
        self._lon:float = lon
        self._time:Optional[str] = time

    def __repr__(self)->str:
        return '<GPXTrackPoint(%f, %f, %s)>'% (self._lat, self._lon, self._time)

    def __str__(self)->str:
        return 'trkpt:%s %s %s'%  (self._lat, self._lon, self._time)

    @property
    def latitude(self)->float:
        return self._lat

    @property
    def longitude(self) -> float:
        return self._lon


    @property
    def time(self, converter:Callable = parse_time)-> Optional[datetime]:
        try:
            return converter(self._time)
        except (TypeError, ValueError):
            return None


    def to_xml(self)->str:
        result:List[str] = ['\n<trkpt lat="%f" lon="%f">'% (self._lat,self._lon),]
        if  self.time:
            result.extend(['\n<time>', self._time, '</time>'])
        result.append('\n</trkpt>')
        return ''.join(result)


    def time_difference(self,other_point:'GPXTrackPoint')->Optional[float]:
        """
        Computes time difference between the points, if both points has time attribute,
        otherwise returns None.

        :other_point:
        :return:  time difference in seconds
        """
        time1:Optional[datetime] = self.time
        time2:Optional[datetime] =other_point.time
        if not self.time or not other_point.time:
            return None

        if time1 == time2:
            return 0
        delta:timedelta = time1 - time2 if time1 > time2 else time2 - time1
        return delta.total_seconds()

    def speed_between(self,other_point:'GPXTrackPoint')->Optional[float]:
        """
         Computes speed betwee two points, if both points have time attribute,
         returns None otherwise.
         :param other_point:
         :return: speed between the points in m/sec
         """
        seconds:float = self.time_difference(other_point)
        if not seconds:
            return  None

        length:float = self.distance_2d(other_point)
        return length / seconds

    def distance_2d(self,other_point:'GPXTrackPoint')->float:
        """
        Computes 2d distance between two points.

        :param other_point:
        :return: distance in meters
        """
        ONE_DEGREE:float = 1000. * 10000.8 / 90.
        coef:float = cos(self.latitude / 180. * pi)
        x:float = self.latitude - other_point.latitude
        y:float = (self.longitude - other_point.longitude) * coef
        return sqrt(x * x + y * y) * ONE_DEGREE



if __name__ == '__main__':
    p0 = GPXTrackPoint(70.016978, 41.3749454, '2016-12-22T11:50:02Z')
    print('p0: point with time: ',p0)
    p1 = GPXTrackPoint(70.024596, 41.4547907,'2017-02-22T07:25:02Z')
    print('p1:point with time: ', p1)
    print('p1.latitude=%s, p1.longitude=%s, p1.time=%s'%( p1.latitude, p1.longitude, p1.time))

    p2 = GPXTrackPoint(70.6978, 41.0749454)
    print('Point without time: ',p2)
    print('p2.time=',p2.time)

    print('p0.time_difference(p1) =', p0.time_difference(p1))
    print('p0.time_difference(p2) =', p0.time_difference(p2))

    print('p0.distance_2d(p1) =', p0.distance_2d(p1))
    print('p0.distance_2d(p2) =', p0.distance_2d(p2))

    print('p0.speed_between(p1) =', p0.speed_between(p1))
    print('p0.speed_between(p2) =', p0.speed_between(p2))
    print(p1.to_xml())
    print(p2.to_xml())
