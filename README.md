# tupleannot

binary data annotation for static typing

* Primitives
  * Int8, 16, 32, 64
  * UInt8, 16, 32, 64
  * Float, Double
* All value is typed array that has one element or more
* Collection
  * Typed Array(fixed length elements)
  * Typed Array(variable length elements. array elment has variable size tuple)
  * Tuple

```python
# variable size Tuple
class VariableSize:
    count: UInt32
    values: Float[-1] # negative size reference sibling value
```

## Usage

```python
import unittest
import struct
from tupleannot import *


# type definition
class Vec3(TypedTuple):
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
```
