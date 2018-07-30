from xml.etree import ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem


gpx = ET.Element('gpx')
trk = ET.SubElement(gpx, 'trk')
trkseg = ET.SubElement(trk, 'trkseg')
trkpt = ET.SubElement(trkseg, 'trkpt', {'lat': '12.34566', 'lon':'84.36736'})
time = ET.SubElement(trkpt, 'time')
time.text =  '2016-12-22T11:50:02.234Z'
ET.dump(indent(gpx))

#<a><b /><c><d /></c></a>