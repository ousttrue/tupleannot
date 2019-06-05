import unittest
from tupleannot import *


# type definition
class Vec3(Tuple):
    x: Float
    y: Float
    z: Float


class SampleTest(unittest.TestCase):
    def test_sample(self):
        # binary data
        import struct
        data = struct.pack('ffffffd', 1, 2, 3, 4, 5, 6, 7)

        # parse / get value
        vec3, remain = Vec3[2].parse(data) # consume bytes
        self.assertEquals(1, vec3[0]['x'])
        self.assertEquals(2, vec3[0]['y'])
        self.assertEquals(3, vec3[0]['z'])
        self.assertEquals(4, vec3[1]['x'])
        self.assertEquals(5, vec3[1]['y'])
        self.assertEquals(6, vec3[1]['z'])

        d, remain = Double.parse(remain)
        self.assertEquals(bytes(), remain)
        self.assertEquals(7, d.value())

        # # to json
        # self.assertEquals('{"x":1,"y":2,"z":3}', vec3.to_json())

        # # from json
        # import json
        # dict_value = json.loads(json_str)
        # vec3.from_dict(**dict_value)
        # self.assertEquals(data, vec3.segments)
