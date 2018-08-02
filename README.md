# gpx-lite
Simple parser for gps tracks, based on
https://pypi.org/project/gpxpy/

Gpx-lite is a simplified version of gpxpy, aimed to load and save data about gpx tracks, segments,
and points from/to xml, including large .gpx files, quickly enough.

Parser only collects data from trk, trkseg, and trkpt gpx tags. All other tags are ignored. 
Resulting GPX structure contains track list - list of track segments made of track points with latitude, 
longitude, and time.  

For more information see https://github.com/aicenter/gpx_lite/wiki

### Prerequisites
Python 3.4 or higher

Typing 3.6.2

### Installation
```commandline
pip install gpx-lite
```




