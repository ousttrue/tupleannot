import struct
import collections
from typing import List, Tuple
try:
    from .primitive import *
except ImportError as ex:
    from primitive import *

VERSION = [0, 1, 0]


class MetaTuple(MetaDefinition):
    def __new__(metacls, name, bases, namespace, **kwds):
        annotations = namespace.get('__annotations__')
        if annotations:
            #print(f'tuple: {name}')
            element_size = 0
            for k, v in annotations.items():
                element_size += v.__element_size__

            # Create Tuple
            class _Tuple(Base, metaclass=MetaDefinition):
                __element_size__ = element_size
                __tuple_items__ = annotations

                def __init__(self, segment: bytes,
                             parent: ParentWithIndex) -> None:
                    super().__init__(segment, parent)
                    self.values: List[Base] = []

                def index_from_key(self, key: str):
                    for i, (k, v) in enumerate(
                            self.__class__.__tuple_items__.items()):
                        if k == key:
                            return i

                def __getitem__(self, key: str):
                    index = self.index_from_key(key)
                    return self.values[index].value()

                def value(self):
                    return {
                        k: x.value()
                        for x, (
                            k,
                            v) in zip(self.values,
                                      self.__class__.__tuple_items__.items())
                    }

                @classmethod
                def parse(cls, data: bytes,
                          parent=None) -> Tuple[bytes, bytes]:
                    src = data
                    size = 0
                    instance = cls(data[0:size], parent)
                    for i, (k, v) in enumerate(annotations.items()):
                        parsed, src = v.parse(src, ParentWithIndex(instance, i))
                        size += len(src)
                        instance.values.append(parsed)
                    return instance, src

            return _Tuple
        else:
            return type.__new__(metacls, name, bases, dict(namespace))


class TypedTuple(metaclass=MetaTuple):
    pass


def main():
    data = struct.pack('6I', 1, 2, 3, 4, 5, 6)
    parsed, remain = UInt32.parse(data)
    print(f'UInt32: {parsed.value()}')

    parsed, remain = UInt32[2].parse(data)
    print(f'Uint32[2]: {parsed.value()}')

    class Vec3(TypedTuple):
        x: UInt32
        y: UInt32
        z: UInt32

    parsed, remain = Vec3.parse(data)
    print(f'remain: {remain}')
    print(f'vec3: {parsed.value()}')

    parsed, remain = Vec3[2].parse(data)
    print(f'parsed[0]["x"]: {parsed[0]["x"]}')

    # data = struct.pack('B2I', 2, 1, 2)
    # class Val(Base):
    #     n: UInt8
    #     values: UInt32[-1]

    # parsed, remain = Val.parse(data)

    # parsed, remain = UInt32.parse(data)


if __name__ == '__main__':
    main()