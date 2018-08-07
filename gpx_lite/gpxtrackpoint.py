from datetime import datetime
from typing import Callable, List, IO

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

    def __init__(self, lat: float, lon: float, time: str) -> None:
        """
        :param lat: point latitude
        :param lon: point longitude
        :param time: time
        """
        self._lat: float = lat
        self._lon: float = lon
        self._time: str = time

    def __eq__(self, other: 'GPXTrackPoint') -> bool:
        if self._lat != other._lat:
            return False
        if self._lon != other._lon:
            return False
        if self._time != other._time:
            return False
        return True

    def time_difference(self, track_point):
        #code from https://github.com/tkrajina/gpxpy/tree/master/gpxpy
        """
        Get time difference between specified point and this point.
        Parameters
        ----------
        track_point : GPXTrackPoint
        Returns
        ----------
        time_difference : float
            Time difference returned in seconds
        """
        if not self.time or not track_point or not track_point.time:
            return None

        time_1 = self.time
        time_2 = track_point.time

        if time_1 == time_2:
            return 0

        if time_1 > time_2:
            delta = time_1 - time_2
        else:
            delta = time_2 - time_1

        if delta is None:
            return None
        return (delta.days * 86400) + delta.seconds

    def __repr__(self) -> str:
        return '<GPXTrackPoint(%f, %f, %s)>' % \
               (self._lat, self._lon, self._time)

    def __str__(self) -> str:
        return 'trkpt:%s %s %s' % (self._lat, self._lon, self._time)

    @property
    def latitude(self) -> float:
        return self._lat

    @property
    def longitude(self) -> float:
        return self._lon

    @property
    def time(self, parser: Callable = parse_time) -> datetime:
        return parser(self._time)

    def to_xml(self) -> str:
        return "\n<trkpt lat=\"{}\" lon=\"{}\">\n<time>{}</time>\n</trkpt>".format(self._lat, self._lon, self._time)

    def to_xml_old(self) -> str:
        print("depricated!")
        return ''.join(['\n<trkpt lat="%f" lon="%f">'
                        % (self._lat, self._lon),
                        '\n<time>', self._time,
                        '</time>\n</trkpt>'])

    def _write_to_file(self, fh: IO) -> None:
        fh.write(self.to_xml())


if __name__ == '__main__':
    p0 = GPXTrackPoint(70.016978, 41.3749454,
                       '2016-12-22T11:50:02Z')
    print('p0: ', p0)
    p1 = GPXTrackPoint(70.024596, 41.4547907,
                       '2017-02-22T07:25:02Z')

    p2 = GPXTrackPoint(70.016978, 41.3749454,
                       '2016-12-22T11:50:02Z')
    print('p1:', p1)
    print('p1.latitude=%s, p1.longitude=%s, p1.time=%s' %
          (p1.latitude, p1.longitude, p1.time))
    print(p0.to_xml())
    print(p0.to_xml_old())
    print(p0.to_xml() == p0.to_xml_old())

    print(p0 == p2)
    print(p1 == p2)
