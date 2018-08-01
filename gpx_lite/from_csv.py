from typing import Dict, Tuple, Iterator, List, Union, Iterable
from tqdm import tqdm
from os import path, listdir

from gpx_lite.gpx import GPX
from gpx_lite.gpxtrackpoint import GPXTrackPoint
from gpx_lite.gpxtracksegment import GPXTrackSegment
from gpx_lite.gpxtrack import GPXTrack

import roadmaptools.inout
from tqdm import tqdm


def read_data_from_csv(filepath: str, gpx: GPX, id_dict: Dict[str, int])->None:
    """
    Loads data from .csv file to gpx object.

    :param filepath:
    :param gpx:
    :param id_dict: dictionary, maps car_id to track position in gpx tracks list.
    :return:
    """
    for row in roadmaptools.inout.load_csv(filepath):
        car_id = row[1]
        point = GPXTrackPoint(float(row[3]), float(row[4]), row[5])
        if car_id not in id_dict.keys():
            num = len(id_dict)
            id_dict[car_id] = num
            gpx.append(GPXTrack(car_id, str(num), [GPXTrackSegment([point,]),]))
        else:
            num = id_dict[car_id]
            gpx[num][0].append(point)



if __name__=='__main__':
    dir:str = '/home/olga/Documents/GPX/csv_data_liftago2'
    filenames: List[str] = [path.join(dir, fn) for fn in listdir(dir)]
    gpx:GPX = GPX()
    id_dict:Dict[str, int] = {}
    with tqdm(filenames, total=len(filenames), desc="Loading csv", unit='files') as pbar:
        for fn in filenames:
            read_data_from_csv(fn, gpx, id_dict)
            pbar.update(1)
            pbar.set_postfix(file=path.basename(fn), refresh=False)

    total_size = sum(map(lambda tr: len(tr), gpx))
    with tqdm(total=total_size, desc='Sorting points in segments', unit='segment') as pbar:
        for tr in gpx:
            for seg in tr:
                seg.sort_by_time()
                pbar.update(1)
            #tr[0].sort_by_time()

    with open('/home/olga/Documents/GPX/liftago2.gpx', 'w') as fh:
        gpx.write_to_file(fh)

