from random import uniform as uf, randrange
from gpx_lite.gpxtrackpoint import GPXTrackPoint as TP



def random_latitude()->float:
    #return float('%.7f'% uf(-90,90))
    return round(uf(-90, 90), 7)

def random_longitude()->float:
    #return float('%.7f'% uf(-180,180))
    return round(uf(-180, 180), 7)

def random_time()->str:
    month = str2(randrange(1,13))
    day = str2(randrange(1,28))
    hour = str2(randrange(24))
    minute = str2(randrange(60))
    sec = str2(randrange(60))
    return '2018-%s-%sT%s:%s:%sZ'% (month, day, hour, minute, sec)

def str2(num:int)->str:
    return str(num) if num >= 10 else '0' + str(num)

def random_point(with_time=True)->TP:
    lat:float = random_latitude()
    lon:float = random_longitude()
    if not with_time:
        return TP(lat, lon)
    time:str = random_time()
    return TP(lat, lon, time)
