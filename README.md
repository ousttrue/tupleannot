# tupleannot

binary data annotation for static typing

* Primitives
  * Int8, 16, 32, 64
  * UInt8, 16, 32, 64
  * Float, Double
* All value is typed array that has one element or more
* Collection
  * Typed Array(fixed length elements)
  * Typed Array(variable length elements)
  * Tuple

## Usage

```python
import unittest
import json
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

        # parse / get value
        remain = vec3.parse(data) # consume bytes
        self.assertEquals(1, vec3['x'])
        self.assertEquals(2, vec3['y'])
        self.assertEquals(3, vec3['z'])

        # serialize
        self.assertEquals(data, vec3.to_bytes())

        # to json
        self.assertEquals('{"x":1,"y":2,"z":3}', vec3.to_json())

        # from json
        dict_value = json.loads(json_str)
        vec3.from_dict(**dict_value)
        self.assertEquals(data, vec3.to_bytes())
```
