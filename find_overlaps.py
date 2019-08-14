import sys
import json
import string
import jsonpickle
from collections import defaultdict
from urllib.request import urlopen
from proto.BulkOrPlanetoid_pb2 import BulkOrPlanetoid

from octant_to_latlong import octant_to_latlong
from octant_to_latlong import LatLonBox

PLANET = "earth"
URL_PREFIX = f"https://kh.google.com/rt/{PLANET}/"


def urlread(url):
    with urlopen(url) as f:
        return f.read()


def read_protobuf(url):
    data = BulkOrPlanetoid()
    data.ParseFromString(urlread(url))
    return data


def read_planetoid_metadata():
    url = URL_PREFIX + "PlanetoidMetadata"
    return read_protobuf(url)


def read_bulk_metadata(path, epoch):
    url = URL_PREFIX + f"BulkMetadata/pb=!1m2!1s{path}!2u{epoch}"
    return read_protobuf(url)


def find_octant_geo_data(octant_per_latlong, midpoint):
    index = 0
   # print("length: " + str(len(octant_per_latlong)))
    for item in octant_per_latlong:
        if item.mid_point.toString() == midpoint.toString():
            return index
        index += 1
    return -1

def parse_path_id(path_id):
    def split_bits(x, n):
        mask = (1 << n) - 1
        return x >> n, x & mask

    path_id, level = split_bits(path_id, 2)

    path_segments = list()
    for _ in range(level + 1):
        path_id, x = split_bits(path_id, 3)
        path_segments.append(x)

    return path_segments, path_id


class NodeData(object):
    def __init__(self, bulk_path, path_id):
        path_segments, flags = parse_path_id(path_id)
        path_string = ''.join(str(x) for x in path_segments)

        self.path = bulk_path + path_string
        self.flags = flags

    def is_bulk(self):
        return (len(self.path) % 4 == 0) and (not (self.flags & 4))

    @staticmethod
    def from_bulk_data(bulk):
        bulk_path = bulk.head_node.path
        return [NodeData(bulk_path, x.path_id) for x in bulk.data]


class OverlappingOctants(object):
    def __init__(self, box):
        self.box = box
        self.list = defaultdict(list)

    def __getitem__(self, level):
        return self.list[level]

    def is_overlapping(self, node_data):
        node_box = octant_to_latlong(node_data.path)
        return LatLonBox.is_overlapping(node_box, self.box)

    def update_bulk_data(self, bulk):
        for node in NodeData.from_bulk_data(bulk):
            if self.is_overlapping(node):
                self.list[len(node.path)].append(node)

class PrintableBoundingBox(object):
    def __init__(self, box):
        self.north_west = PrintableLatLon([ box[0], box[2] ])
        self.south_east = PrintableLatLon([ box[1], box[3] ])

class PrintableLatLon(object):
    def __init__(self, latlon):
        self.latitude = latlon[0]
        self.longitude = latlon[1]

    def toString(self):
        return str(self.latitude) + ", " + str(self.longitude)

class OctantGeoData(object):
    def __init__(self, box, octants):
        self.mid_point = PrintableLatLon(box.mid_point)
        self.bbox = PrintableBoundingBox(box)
        self.octants = octants

class LevelOctantGeoData(object):
    def __init__(self, level, octantGeoDatas):
        self.level = level
        self.octantGeoDatas = octantGeoDatas


MAX_COUNT = 100

input_box = sys.argv[1:5]
input_box = LatLonBox(*(float(x) for x in input_box))

max_level = int(sys.argv[5])

overlapping_octants = OverlappingOctants(input_box)

planetoid_metadata = read_planetoid_metadata()
epoch = planetoid_metadata.data[0].epoch
bulk = read_bulk_metadata('', epoch)

overlapping_octants.update_bulk_data(bulk)

octant_per_latlong = []
for level in range(1, max_level + 1):
    octant_per_latlong.append([])
    for octant in overlapping_octants[level]:
        bbox = octant_to_latlong(octant.path)
        index = find_octant_geo_data(octant_per_latlong[level - 1], bbox.mid_point)
        if index < 0:
            octant_per_latlong[level - 1].append(OctantGeoData(bbox, [ octant.path ]))
        else:
            octant_per_latlong[level - 1][index].octants.append(octant.path)

    for octant in overlapping_octants[level]:
        if octant.is_bulk():
            bulk = read_bulk_metadata(octant.path, epoch)
            overlapping_octants.update_bulk_data(bulk)

print(json.dumps(json.loads(jsonpickle.encode(octant_per_latlong, unpicklable=False)), indent=4))
