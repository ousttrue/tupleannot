import unittest
from tupleannot import *


class SampleTest(unittest.TestCase):
    def test_sample(self):
        # binary data
        import struct
        data = struct.pack('ffffffd', 1, 2, 3, 4, 5, 6, 7)

        # type definition
        vec3 = Tuple('Vec3', [
            Float('x'),
            Float('y'),
            Float('z'),
        ])

        # parse / get value
        remain = vec3.parse(data) # consume bytes
        self.assertEquals(1, vec3['x'])
        self.assertEquals(2, vec3['y'])
        self.assertEquals(3, vec3['z'])

        remain = vec3.parse(remain) # consume bytes

        d = Double('d')
        remain = d.parse(remain)
        self.assertEquals(bytes(), remain)
        self.assertEquals(7, d.value())

        # # to json
        # self.assertEquals('{"x":1,"y":2,"z":3}', vec3.to_json())

        # # from json
        # import json
        # dict_value = json.loads(json_str)
        # vec3.from_dict(**dict_value)
        # self.assertEquals(data, vec3.segments)
