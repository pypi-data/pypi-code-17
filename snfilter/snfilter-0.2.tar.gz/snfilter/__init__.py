import requests
import logging
import json
import sys
import csv
import io

log = logging.getLogger(__name__)

gr_feed_preamble = """

Refresh: 1
Threshold: 999
Title: Spotter Network Positions - {filtername}
Font: 1, 11, 0, "Courier New"
IconFile: 1, 22, 22, 11, 11, "http://www.spotternetwork.org/icon/spotternet.png"
IconFile: 2, 15, 25, 8, 25, "http://www.spotternetwork.org/icon/arrows.png"
IconFile: 6, 22, 22, 11, 11, "http://www.spotternetwork.org/icon/spotternet_new.png"

"""

def output_json(objects, indent=None):
    return json.dumps(objects, indent=indent)

def output_truvu(objects):
    with io.StringIO() as f:
        w = csv.DictWriter(f, fieldnames=["ID", "Station Name", "Latitude", "Longitude", "Temperature", "Weather"])
        w.writerow({"ID":"ID","Station Name":"Station Name","Latitude":"Latitude","Longitude":"Longitude","Temperature":"Temperature","Weather":"Weather"})
        c = 0
        for o in objects:
            c += 1
            d = {
                "ID":c,
                "Station Name": o["name"],
                "Latitude": o["lat"],
                "Longitude": o["lon"],
                "Temperature": "55",
                "Weather": "Sunny"
            }
            w.writerow(d)
        f.seek(0)
        return "".join(f.readlines())

def output_gr(objects, filtername="snfilter"):
    output = gr_feed_preamble.format(filtername=filtername)
    for o in objects:
        for l in o["origlines"]:
            output = output + l + "\n"
        output = output + "\n"
    return output

def parse_nameslist(nameslist):
    names = list()
    xlator = dict()
    individuals = nameslist.split(",")
    for i in individuals:
        iparts = i.split(":")
        names.append(iparts[0])
        if len(iparts) == 2:
            xlator[iparts[0]] = iparts[1]
    return names, xlator

def filter_feed(raw_feed, names, translator=dict()):
    all_objects = parse_raw_feed(raw_feed)
    filtered_objects = filter_objects_byname(all_objects, names)
    filtered_objects = translate_objects(filtered_objects, translator=translator)
    return filtered_objects
    # translated_objects = (invoke function that translates the names)
    # return filtered and translated list

def translate_objects(objects, translator=dict()):
    for o in objects:
        if o["name"] in translator:
            o["name"] = translator[o["name"]]
    return objects

def parse_objectlines(olines):
    log.debug("parsing a set of object lines")
    #parse the individual lines of the object
    #build up a datastructure of the elements
    ds = dict()
    ds["origlines"] = olines
    ds["icons"] = list()

    for l in olines:
        if l.startswith("Object:"):
            oparts = l.split(":")
            if len(oparts) == 2:
                llparts = oparts[1].split(",")
                if len(llparts) == 2:
                    ds['lat'] = float(llparts[0])
                    ds['lon'] = float(llparts[1])
        if l.startswith("Text:"):
            tparts = l.split(",")
            if len(tparts) == 4:
                ds["name"] = tparts[3].strip('"').lstrip(" ").lstrip("\"")
        if l.startswith("Icon:"):
            ds['icons'].append(parse_iconline(l))
    return ds

def parse_iconline(line):
    d = dict()
    d["origline"] = line
    # the following line is what we're looking for here, it's got some useful
    # info we want to tease out
    # Icon: 0,0,000,6,10,"Brandon Oboikovitz\n2017-04-30 20:16:22 UTC\nSTATIONARY\nPhone: 8153023601\nEmail: brandon59316@gmail.com"
    # split out the icon part
    parts1 = line.split("Icon: ")
    # split out the properties
    parts2 = parts1[1].split(",")
    if len(parts2) == 6:
        # we've got some interesting info to pick out if 6 elements
        # we want this parts and split on \n
        # "Brandon Oboikovitz\n2017-04-30 20:16:22 UTC\nSTATIONARY\nPhone: 8153023601\nEmail: brandon59316@gmail.com"
        parts3 = parts2[5].lstrip('"').rstrip('"').split("\\n")
        if len(parts3) >= 3:
            d["desc"] = parts3[0]
            d["last_beacon"] = parts3[1]
            d["heading"] = parts3[2]
            if len(parts3) > 3:
                # not we split out the extra stuff
                for p in parts3[3:]:
                    parts4 = p.split(': ')
                    d[parts4[0]] = parts4[1]
    return d

def parse_raw_feed(raw):
    lines = raw.split("\n")
    # build up chunks of the data structure, we need to takes lines between
    # object and end and pass those to the chunk parser
    objects = list()
    objectlines = list()
    have_object = False
    for l in lines:
        log.debug("line is: \"%s\"", l)
        log.debug("have_object var is %s", have_object)
        l = l.strip()
        if l.startswith("Object:"):
            log.debug("have an object now")
            have_object = True
        if have_object:
            log.debug("adding line to object")
            objectlines.append(l)
            if l.startswith("End"):
                log.debug("end of object")
                have_object = False
                objects.append(parse_objectlines(objectlines))
                objectlines = list()
    return objects

def filter_objects_byname(objects, namelist):
    lower_names = [ x.lower() for x in namelist ]
    filtered = list()
    for o in objects:
        if o["name"].lower() in lower_names:
            filtered.append(o)
    return filtered
