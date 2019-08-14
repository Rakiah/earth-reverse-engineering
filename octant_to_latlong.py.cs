
using namedtuple = collections.namedtuple;

using System.Collections.Generic;

public static class octant_to_latlong {
    
    public static object octant_dict = new Dictionary<object, object> {
        {
            "0",
            Tuple.Create(0, 0, 0)},
        {
            "1",
            Tuple.Create(1, 0, 0)},
        {
            "2",
            Tuple.Create(0, 1, 0)},
        {
            "3",
            Tuple.Create(1, 1, 0)},
        {
            "4",
            Tuple.Create(0, 0, 1)},
        {
            "5",
            Tuple.Create(1, 0, 1)},
        {
            "6",
            Tuple.Create(0, 1, 1)},
        {
            "7",
            Tuple.Create(1, 1, 1)}};
    
    public class LatLon
        : namedtuple("LatLon",["lat","lon"]) {
        
        public virtual object toString() {
            var _tup_1 = tuple(this);
            var lat = _tup_1.Item1;
            var lon = _tup_1.Item2;
            return lat.ToString() + ", " + lon.ToString();
        }
    }
    
    public class LatLonBox
        : namedtuple("LatLonBox",["north","south","west","east"]) {
        
        public object mid_point {
            get {
                var _tup_1 = tuple(this);
                var n = _tup_1.Item1;
                var s = _tup_1.Item2;
                var w = _tup_1.Item3;
                var e = _tup_1.Item4;
                return LatLon((n + s) / 2, (w + e) / 2);
            }
        }
        
        public virtual object get_child(object octant) {
            try {
                var _tup_1 = octant_dict[octant];
                var oct_x = _tup_1.Item1;
                var oct_y = _tup_1.Item2;
                var oct_z = _tup_1.Item3;
            } catch (KeyError) {
                throw ValueError("invalid octant value");
            }
            var _tup_2 = tuple(this);
            var n = _tup_2.Item1;
            var s = _tup_2.Item2;
            var w = _tup_2.Item3;
            var e = _tup_2.Item4;
            if (oct_y == 0) {
                n = this.mid_point.lat;
            } else if (oct_y == 1) {
                s = this.mid_point.lat;
            } else {
                throw ValueError;
            }
            if (n == 90 || s == -90) {
                return LatLonBox(n, s, w, e);
            }
            if (oct_x == 0) {
                e = this.mid_point.lon;
            } else if (oct_x == 1) {
                w = this.mid_point.lon;
            } else {
                throw ValueError;
            }
            return LatLonBox(n, s, w, e);
        }
        
        public virtual object toString() {
            var _tup_1 = tuple(this);
            var n = _tup_1.Item1;
            var s = _tup_1.Item2;
            var w = _tup_1.Item3;
            var e = _tup_1.Item4;
            return n.ToString() + ", " + w.ToString() + ", " + s.ToString() + ", " + e.ToString();
        }
        
        [staticmethod]
        public static object is_overlapping(object box1, object box2) {
            var _tup_1 = box1;
            var n1 = _tup_1.Item1;
            var s1 = _tup_1.Item2;
            var w1 = _tup_1.Item3;
            var e1 = _tup_1.Item4;
            var _tup_2 = box2;
            var n2 = _tup_2.Item1;
            var s2 = _tup_2.Item2;
            var w2 = _tup_2.Item3;
            var e2 = _tup_2.Item4;
            var n = min(n1, n2);
            var s = max(s1, s2);
            var w = max(w1, w2);
            var e = min(e1, e2);
            return n >= s && w <= e;
        }
    }
    
    public static object first_latlonbox_dict = new Dictionary<object, object> {
        {
            "",
            LatLonBox(90, -90, -180, 180)},
        {
            "0",
            LatLonBox(0, -90, -180, 0)},
        {
            "1",
            LatLonBox(0, -90, 0, 180)},
        {
            "2",
            LatLonBox(90, 0, -180, 0)},
        {
            "3",
            LatLonBox(90, 0, 0, 180)},
        {
            "02",
            LatLonBox(0, -90, -180, -90)},
        {
            "03",
            LatLonBox(0, -90, -90, 0)},
        {
            "12",
            LatLonBox(0, -90, 0, 90)},
        {
            "13",
            LatLonBox(0, -90, 90, 180)},
        {
            "20",
            LatLonBox(90, 0, -180, -90)},
        {
            "21",
            LatLonBox(90, 0, -90, 0)},
        {
            "30",
            LatLonBox(90, 0, 0, 90)},
        {
            "31",
            LatLonBox(90, 0, 90, 180)}};
    
    public static object octant_to_latlong(object octant_string) {
        var latlonbox = first_latlonbox_dict[octant_string[0::2]];
        foreach (var octant in octant_string[2]) {
            latlonbox = latlonbox.get_child(octant);
        }
        return latlonbox;
    }
}
