# tupleannot

binary data annotation for static typing

* Primitives
  * Int8, 16, 32, 64
  * UInt8, 16, 32, 64
  * Float, Double
* Collection
  * Typed Array
    * array length
      * fixed
      * lazy(length is stored in previous value)
    * element length
      * fixed
      * variable(contain lazy length array)
* Tuple

## Usage

### type definition

```python
# type definition
class Vec3(TypedTuple):
    x: Float
    y: Float
    z: Float

# binary data
data = struct.pack('ffffffd', 1, 2, 3, 4, 5, 6, 7)

# parse
vec3, remain = Vec3[2].parse(data) # consume bytes

# parsed
self.assertEqual(1, vec3[0]['x'])
self.assertEqual(2, vec3[0]['y'])
self.assertEqual(3, vec3[0]['z'])
self.assertEqual(4, vec3[1]['x'])
self.assertEqual(5, vec3[1]['y'])
self.assertEqual(6, vec3[1]['z'])
```

### lazy array length

```python
class Val(TypedTuple):
    length: UInt8
    values: UInt32[-1] # determinate array length by relative value

data = struct.pack('<B2I', 2, 1, 2)

parsed, remain = Val.parse(data)
```

### variable element length

```python
class Val(TypedTuple):
    length: UInt8
    values: Vec3[-1] # determinate array length by relative value

class VariableLengthArray(TypedTuple):
    tuple_items: Val[2] # item length is variable
```
