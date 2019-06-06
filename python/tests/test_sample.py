import unittest
import struct
from tupleannot import *


# type definition
class Vec3(TypedTuple):
    x: FloatLE
    y: FloatLE
    z: FloatLE


class SampleTest(unittest.TestCase):
    def test_sample(self):
        # binary data
        data = struct.pack('<ffffffd', 1, 2, 3, 4, 5, 6, 7)

        # parse / get value
        vec3, remain = Vec3[2].parse(data) # consume bytes
        self.assertEqual(1, vec3[0]['x'].value())
        self.assertEqual(2, vec3[0]['y'].value())
        self.assertEqual(3, vec3[0]['z'].value())
        self.assertEqual(4, vec3[1]['x'].value())
        self.assertEqual(5, vec3[1]['y'].value())
        self.assertEqual(6, vec3[1]['z'].value())

        d, remain = DoubleLE.parse(remain)
        self.assertEquals(bytes(), remain)
        self.assertEquals(7, d.value())

        # # to json
        # self.assertEquals('{"x":1,"y":2,"z":3}', vec3.to_json())

        # # from json
        # import json
        # dict_value = json.loads(json_str)
        # vec3.from_dict(**dict_value)
        # self.assertEquals(data, vec3.segments)
