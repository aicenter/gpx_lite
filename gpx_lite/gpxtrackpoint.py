from datetime import datetime
from typing import Callable, List

from gpx_lite.utils import parse_time


class GPXTrackPoint:
    """
    Track point, leaf element of gpx

    Attributes:
        latitude: float
        longitude: float
        time:   datetime

    """

    __slots__ = ('_lat', '_lon', '_time')

    def __init__(self, lat: float, lon: float, time: str)->None:
        """
        :param lat: point latitude
        :param lon: point longitude
        :param time: time
        """
        self._lat: float = lat
        self._lon: float = lon
        self._time: str = time

    def __repr__(self)->str:
        return '<GPXTrackPoint(%f, %f, %s)>' % \
               (self._lat, self._lon, self._time)

    def __str__(self)->str:
        return 'trkpt:%s %s %s' % (self._lat, self._lon, self._time)

    @property
    def latitude(self)->float:
        return self._lat

    @property
    def longitude(self) -> float:
        return self._lon

    @property
    def time(self, parser: Callable = parse_time)->datetime:
        return parser(self._time)

    def to_xml(self)->str:
        """

        :return: point as xml string
        """
        result:List[str] = ['\n<trkpt lat="%f" lon="%f">' % (self._lat,self._lon),
                            '\n<time>', self._time, '</time>','\n</trkpt>']
        return ''.join(result)


if __name__ == '__main__':
    p0 = GPXTrackPoint(70.016978, 41.3749454, '2016-12-22T11:50:02Z')
    print('p0: ',p0)
    p1 = GPXTrackPoint(70.024596, 41.4547907,'2017-02-22T07:25:02Z')
    print('p1:', p1)
    print('p1.latitude=%s, p1.longitude=%s, p1.time=%s'%( p1.latitude, p1.longitude, p1.time))
    print(p1.to_xml())
