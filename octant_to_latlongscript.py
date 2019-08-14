import sys
from octant_to_latlong import octant_to_latlong
from octant_to_latlong import LatLonBox

input_octant = sys.argv[1]
print(octant_to_latlong(input_octant).mid_point)
