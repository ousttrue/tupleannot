# tupleannot

binary data serializer for static typing

* Primitives
    * Int8, 16, 32, 64
    * UInt8, 16, 32, 64
    * Float, Double
* All value is typed array that has one element or more
* Collection
    * Typed Array
    * Typed Array that has variable length elements

## Usage

```python
# binary data
data = struct.pack('fff', [1, 2, 3])

# type definition
vec3 = Tuple('Vec3', 1, False, [
    Float('x'),
    Float('y'),
    Float('z'),
])

# parse
vec3.parse(data)

# deserialize
vec3['x'] # 1
vec3['y'] # 2
vec3['z'] # 3
```
