import unittest
import struct
from tupleannot import *


# type definition
class Vec3(Base):
    x: Float
    y: Float
    z: Float


class SampleTest(unittest.TestCase):
    def test_sample(self):
        # binary data
        data = struct.pack('ffffffd', 1, 2, 3, 4, 5, 6, 7)

        # parse / get value
        vec3, remain = Vec3[2].parse(data) # consume bytes
        self.assertEqual(1, vec3[0]['x'])
        self.assertEqual(2, vec3[0]['y'])
        self.assertEqual(3, vec3[0]['z'])
        self.assertEqual(4, vec3[1]['x'])
        self.assertEqual(5, vec3[1]['y'])
        self.assertEqual(6, vec3[1]['z'])

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
