from typing import Dict, Tuple, Iterator, List, Union


from gpx_lite.gpx import  GPX
from gpx_lite.gpxtrackpoint import GPXTrackPoint
from gpx_lite.gpxtracksegment import GPXTrackSegment
from gpx_lite.gpxtrack import GPXTrack
import roadmaptools.inout
from roadmaptools.printer import print_info
from tqdm import tqdm
from operator import itemgetter
import csv
from time import  process_time

def load_traces_from_csv(filepath: str)->Dict[str, List[Union[float,str]]]:
    trace_dict:Dict[str, List[float,float,str]] = dict()
    line_count:int = len(open(filepath).readlines())
    iterator:Iterator = roadmaptools.inout.load_csv(filepath)
    for row in tqdm(iterator, total=line_count, desc="Parsing traces"):
        if row[0] not in trace_dict:
            trace_dict[row[0]] = []
        trace_dict[row[0]].append([float(row[1]), float(row[2]), row[3]]) # _convert_string_to_time(row[3])])
        # trace_dict[row[0]].append([row[1], row[2], row[3]])
    trace_dict_sorted = {}
    for car_id, trace in tqdm(trace_dict.items(), desc="Sorting points in traces"):
        #print(car_id)
        trace_dict_sorted[car_id] = sorted(trace, key=itemgetter(2))

    return trace_dict_sorted


def export_traces_to_gpx(trips_dict) -> GPX:

    print_info("Creating gpx structure")
    gpx = GPX()

    id_counter = 0
    for key, values in tqdm(trips_dict.items(), desc="Creating tracks"):
        gpx_track = GPXTrack(name=key, number=id_counter)
        gpx.tracks.append(gpx_track)
        gpx_segment = GPXTrackSegment()
        gpx_track.segments.append(gpx_segment)ч

        for point in values:
           # print(type(point[0]), type(point[1]), type(point[2]))
            gpx_segment.points.append(GPXTrackPoint(point[0], point[1], time=point[2]))
        id_counter += 1

    # gpx.extensions = {"id_counter": id_counter}
   # roadmaptools.inout.save_gpx(gpx, config.mapmatching.raw_traces_filepath)

    return gpx

if __name__=='__main__':
    fn = '/home/olga/Documents/GPX/out.c_ltgauxiliary.taxiposition_friday_2017_06_23.csv'
    start = process_time()
    traces = load_traces_from_csv(fn)
    gpx = export_traces_to_gpx(traces)
    print(gpx)
    print(process_time() - start)
    # 1: second converdion = 9.4
    # 2: without           = 8.5