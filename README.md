# tupleannot

binary format experiment

## Usage

```python
data = struct.pack('fff', [1, 2, 3])

vec3 = Tuple('Vec3', 1, False, [
    Float('x'),
    Float('y'),
    Float('z'),
])

vec3.parse(data)

vec3['x'] # 1
vec3['y'] # 2
vec3['z'] # 3
```
