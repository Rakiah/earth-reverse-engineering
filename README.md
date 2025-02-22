[![Gitter Chat](https://badges.gitter.im/earth-reverse-engineering/lobby.svg)](https://gitter.im/earth-reverse-engineering/lobby)

![header](header.png "Header image: 37.793647, -122.398938")

This is an attempt to reverse-engineer undocumented parts of Google Earth. Main goal is to document the results and to provide code that emerges.

#### Earth to OBJ file downloader
We can dump a textured 3D model (*.obj with *.bmp and *.jpg) using the following scripts. They require [Node.js](https://nodejs.org/en/) v8 and [npm](https://www.npmjs.com/):
```sh
# Install dependencies (tested with node@8.15.0, npm@6.4.1)
npm install

# Find octant of latitude and longitude
node lat_long_to_octant.js 37.420806884765625 -122.08419799804688

# Dump octant with max-level 20
node dump_obj.js 20527061605273514 20
```
Exported files will be in `./downloaded_files/obj`. They can be opened in Blender [like this](BLENDER.md).

#### Notes

Alternative method for finding octant: [Open maps and dev tools, switch to satellite, fly to destination, search for NodeData, copy octant path from recent request](how_to_find_octant.jpg)

You can use this to dump json and raw data instead of obj:
```
node dump_obj.js 20527061605273514 20 --dump-json --dump-raw
```

URL structure:
```
"https://kh.google.com/rt/🅐/🅑"
 - 🅐: planet
       - "earth"
       - "mars"
       - ...
 - 🅑: resource
       - "PlanetoidMetadata"
       - "BulkMetadata/pb=!1m2!1s❶!2u❷"
          - ❶: octant path
          - ❷: epoch
       - "NodeData/pb=!1m2!1s❸!2u❹!2e❺(!3u❻)!4b0"
          - ❸: octant path
          - ❹: epoch
          - ❺: texture format
          - ❻: imagery epoch (sometimes)
```

Misc:
```
General info:
 - Everything is stored in an octree.

Roles of resources:
 - PlanetoidMetadata points to first BulkMetaData.
 - BulkMetaData points to other BulkMetaData and to NodeData.
 - NodeData contains actual meshes and textures.

Versioning:
 - BulkMetaData and NodeData are versioned using epoch numbers.
 - PlanetoidMetadata provides epoch of first BulkMetaData.
 - BulkMetaData provides epochs of underlying resources.
 - Current version of a resource can be determined recursively.
 
NodeData:
 - Vertex Buffer:
    - 8 bytes per point: X,Y,Z,W,U,U,V,V
    - XYZ: position, W: octant mask, UV: texture coordinates
 - Texture:
    - Format 1: JPEG
    - Format 6: S3 DXT1 RGB
BulkMetaData:
  - Oriented Bounding Box
    - Dump OBB to obj: https://gist.github.com/retroplasma/5698808bfaa63ffd03f751a84fa6ce14
    - Latlong to octant using OBB (unstable): https://github.com/retroplasma/earth-reverse-engineering/blob/443a3622ce9cb12cd4460cc6dc7999cc703ae67f/experimental_latlong_to_octant.js

TODO:
   - Efficient level of detail and frustum culling (combination of octants, OBB, BVH?)
```

Related ideas: [Racing game](https://www.reddit.com/r/Showerthoughts/comments/aex25s/race_car_video_games_could_be_amazing_if_they/) , [Minimal client](https://github.com/kaylathedev/google-maps-3d-client). WebGL + CORS should work ([test](https://retroplasma.github.io/get_planetoid_metadata.html)).

#### Method for dumping an area:
For this to work you will need:
- Python
- NodeJs
- Shell
- Image magick

./dump_area.sh NORTH WEST SOUTH EAST ZOOM_LEVEL

ex: ./dump_area.sh 48.8711416157 2.2269540256 48.8684591806 2.2323578439 99

which will provide you a folder like [this](./dump_area_image.png)
each sub folder seen in the screenshot will be a full self contained tile composing the area you requested,
in each of the sub folder, you will find a geoData.json, which is a file that contains all informations
needed to place your tiles next to each others (midpoint, bounding box)

#### Png compression
Added a script that will compress using Image Magick converter the bmp images into png files, reducing the final
size of large area by roughly 50%


#### Draco compression
I've also added [draco](https://github.com/google/draco) to try and reduce the size of the areas that can go quite
large, however draco doesn't seem to support multiple meshes which is a big problem in our scenario because tiles
are actually composed of multiple octants that are all a different mesh, the few wrong results of draco seems like
very powerfull however if we can make it work, reducing 60 mb files to 1000Kos file while not loosing all of the data
it contained

#### Important
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
