import unittest
import struct
from tupleannot import *


class TestSample(unittest.TestCase):
    def test_sample(self):
        # binary data
        data = struct.pack('fff', 1, 2, 3)

        # type definition
        vec3 = Tuple('Vec3', [
            Float('x'),
            Float('y'),
            Float('z'),
        ])

        # parse
        vec3.parse(data)

        # deserialize
        self.assertEquals(1, vec3['x'])
        self.assertEquals(2, vec3['y'])
        self.assertEquals(3, vec3['z'])