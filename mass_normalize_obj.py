import sys
import glob
import numpy as np
from pathlib import Path
from tqdm import tqdm

origin = np.array([float(x) for x in sys.argv[1:4]])

radius = np.linalg.norm(origin) #.magnitude

lat = np.arcsin(origin[2] / radius) #arcsin as radian
lon = np.arctan2(origin[1], origin[0]) #atan2

sin_lat = np.sin(lat) #sin
cos_lat = np.cos(lat) #cos
sin_lon = np.sin(lon) #sij
cos_lon = np.cos(lon) #cos

Rz = np.array([[cos_lon, sin_lon, 0], [-sin_lon, cos_lon, 0], [0, 0, 1]]) #matrix z
Ry = np.array([[cos_lat, 0, sin_lat], [0, 1, 0], [-sin_lat, 0, cos_lat]]) #matrix x
R = Ry @ Rz #matmult Ry & Rz

obj_list = glob.glob(sys.argv[4])

for i in obj_list:
    input_file = Path(i)
    output_file = input_file.with_name(input_file.stem + '.2.obj')

    with input_file.open() as in_, output_file.open('w') as out:
        for line in tqdm(in_):
            if line.startswith("v "):
                vertex = np.fromstring(line[2:], sep=' ') #get each vertices
                vertex = R @ (vertex - origin) #multiply matrices with (vertex -origin)
                line = "v {} {} {}\n".format(*vertex)

            out.write(line)
