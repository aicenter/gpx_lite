import timeit
from functools import wraps
from typing import Callable, List
from os import path, listdir
from time import process_time


#from gpxpy.parser import GPXParser as OriginalParser
from gpx_lite.parser import GPXParser as Parser
from gpx_lite.benchmark.test_utils import  make_result_string, get_time
from gpx_lite.gpx import  GPX


MB = 1000*1000


def timer(func:Callable)->Callable:
    @wraps(func)
    def wrapper(*args, **kwargs)->float:
        best_time = min(timeit.Timer(lambda: func(*args, **kwargs)).repeat(repeat=10, number=1))
        print(*args)
        print('%.2f Mbs in %.2f seconds' % (path.getsize(args[0])/MB, best_time))
        return best_time
    return wrapper


@timer
def measure_load1(fname: str)->None:
    with open(fname, 'r') as xml_file:
        parser = Parser(xml_file)
        parser.parse()
        #parser.iterparse()


@timer
def save(fn: str, gpx: GPX, )->None:
    with open(fn, 'w') as fh:
        fh.write(gpx.to_xml())


def measure_save1(fname: str)->None:
    with open(fname, 'r') as xml_file:
        parser = Parser(xml_file)
        gpx = parser.parse()
        save(fname +'.saved.gpx', gpx )


# @timer
# def  measure_load2(fname:str):
#     with open(fname, 'r') as xml_file:
#         parser =  OriginalParser(xml_file)
#     parser.parse()


@timer
def convert_values(gpx_content:GPX):
    all_points = [pt for tr in gpx_content for seg in tr for pt in seg]
    for i in range(10):
        coords = [c for c in map(lambda pt: (pt.latitude, pt.longitude), all_points)]


def measure_conversion(fname: str):
    with open(fname, 'r') as xml_file:
        parser = Parser(xml_file)
        gpx = parser.parse()
        return convert_values(gpx)


def measure_time(func:Callable,
                 test_dir: str,
                 result_dir: str,
                 result_name: str):


    filenames: List[str] = [path.join(test_dir, fn) for fn in listdir(test_dir)]
    filenames.sort(key=lambda fn: path.getsize(fn))

    sizes: List[float] = [round(path.getsize(name)/MB,2) for name in filenames]
    start: float = process_time()
    times: List[float] = [n for n in map(lambda name : func(name), filenames)]
    total_time:float = process_time() - start
    print(times)
    string:str = make_result_string(2, ['Mbs', 'Time'], sizes, times)
    string += '\n\n\nTotal time: {:10.2f} minutes\n'.format(total_time / 60)
    print(string)

    result_fn: str = path.join(result_dir, result_name + get_time() + '.txt')
    with open(result_fn, 'w') as out_file:
        out_file.write(string)


TEST_DIR = "/home/olga/Documents/GPX/load_test"
RESULTS_DIR = "/home/olga/Documents/GPX/test_results"

#measure_time(measure_load1, TEST_DIR, RESULTS_DIR,  'iterparser1_')
#measure_load1("/home/olga/Documents/GPX/traces-raw.gpx") # time =  5.3
#measure_time(measure_load2, TEST_DIR, RESULTS_DIR,  'final_load_other_')
#measure_time(measure_conversion, TEST_DIR, RESULTS_DIR,  'try_except_conv_')
measure_time(measure_save1, TEST_DIR, RESULTS_DIR, '.save_xml')

