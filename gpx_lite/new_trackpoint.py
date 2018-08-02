from datetime import datetime
from typing import Callable, List, IO

from gpx_lite.utils import parse_time, time_to_int, time_to_str


class NewTrackPoint:
    """
    Experimental class for track point,datetime is kept as integer,
    and converted to str or datetime when needed.

    It uses about 30% less RAM for gpx object, and has almost the same time
    for parsing (247 seconds compared to 235 for 3.2 Gb ).
    And  150 sec to save it back to gpx.

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
        self._time: int = time_to_int(time)

    def __eq__(self, other: 'NewTrackPoint')->bool:
        if self._lat != other._lat:
            return False
        if self._lon != other._lon:
            return False
        if self._time != other._time:
            return False
        return True

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
        return parser(time_to_str(self._time))

    def to_xml(self)->str:
        return ''.join(['\n<trkpt lat="%f" lon="%f">'
                        % (self._lat, self._lon),
                        '\n<time>', time_to_str(self._time),
                        '</time>\n</trkpt>'])

    def _write_to_file(self, fh: IO)->None:
        fh.write(self.to_xml())


if __name__ == '__main__':
    p0 = NewTrackPoint(70.016978, 41.3749454,
                       '2016-12-22T11:50:02Z')
    print('p0: ',p0)
    p1 = NewTrackPoint(70.024596, 41.4547907,
                       '2017-02-22T07:25:02Z')

    p2 = NewTrackPoint(70.016978, 41.3749454,
                       '2016-12-22T11:50:02Z')
    print('p1:', p1)
    print('p1.latitude=%s, p1.longitude=%s, p1.time=%s' %
          (p1.latitude, p1.longitude, p1.time))
    print(p0.to_xml())

    print(p0 == p2)
    print(p1 == p2)

