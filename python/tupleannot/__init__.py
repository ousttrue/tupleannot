import struct
import collections
from typing import List, Tuple
try:
    from .primitive import *
    from .string import *
except ImportError as ex:
    from primitive import *
    from string import *

VERSION = [0, 1, 0]


class MetaTuple(MetaDefinition):
    def __new__(metacls, name, bases, namespace, **kwds):
        annotations = namespace.get('__annotations__')
        if annotations:
            #print(f'tuple: {name}')
            def _has_lazy_array():
                for k, v in annotations.items():
                    if v.is_lazy_array():
                        return True
                    if v.is_tuple():
                        if v.has_lazy_array():
                            return True
                return False

            def _value_size():
                element_size = 0
                for k, v in annotations.items():
                    element_size += v.value_size()
                return element_size

            # Create Tuple
            class _Tuple(Base, metaclass=MetaDefinition):
                __tuple_items__ = annotations

                def __init__(self, segment: bytes,
                             parent: ParentWithIndex) -> None:
                    super().__init__(segment, parent)
                    self.values: List[Base] = []

                def __str__(self)->str:
                    return '{' + ', '.join(f'"{k}": {str(v)}' for k, v in self.value().items()) + '}'

                def index_from_key(self, key: str):
                    for i, (k, v) in enumerate(
                            self.__class__.__tuple_items__.items()):
                        if k == key:
                            return i

                def __getitem__(self, key: Any):
                    if isinstance(key, str):
                        key = self.index_from_key(key)
                    return self.values[key]

                def value(self):
                    return {
                        k: x
                        for x, (
                            k,
                            v) in zip(self.values,
                                      self.__class__.__tuple_items__.items())
                    }

                @classmethod
                def has_lazy_array(cls):
                    return _has_lazy_array()

                @classmethod
                def value_size(cls):
                    if _has_lazy_array():
                        raise Exception('not has value_size, because contain lazy array')
                    return _value_size()

                @classmethod
                def parse(cls, data: bytes,
                          parent=None) -> Tuple[bytes, bytes]:
                    src = data
                    size = 0
                    instance = cls(data[0:size], parent)
                    for i, (k, v) in enumerate(annotations.items()):
                        parsed, src = v.parse(src,
                                              ParentWithIndex(instance, i))
                        size += len(parsed.segment)
                        instance.values.append(parsed)
                    instance.segment = data[0:size]
                    return instance, src

            _Tuple.__name__ = name
            return _Tuple
        else:
            return type.__new__(metacls, name, bases, dict(namespace))


class TypedTuple(metaclass=MetaTuple):
    pass


def tuple_sample():
    data = struct.pack('<6I', 1, 2, 3, 4, 5, 6)
    parsed, remain = UInt32LE.parse(data)
    print(f'UInt32: {parsed.value()}')

    parsed, remain = UInt32LE[2].parse(data)
    print(f'UInt32[2]: {parsed}')

    class Vec3(TypedTuple):
        x: UInt32LE
        y: UInt32LE
        z: UInt32LE

    parsed, remain = Vec3.parse(data)
    print(f'remain: {remain}')
    print(f'vec3: {parsed}')

    parsed, remain = Vec3[2].parse(data)
    print(f'parsed[0]["x"]: {parsed[0]["x"]}')


def lazy_length_sample():
    class Val(TypedTuple):
        n: UInt8
        values: UInt32LE[-1]
    data = struct.pack('<B2I', 2, 1, 2)
    print(len(data))
    parsed, remain = Val.parse(data)
    print(f'parsed: {parsed}')

    class VariableLengthArray(TypedTuple):
        tuple_items: Val[2] # item length is variable
    data = struct.pack('<B2IB3I', 2, 1, 2, 3, 4, 5, 6)
    parsed, remain = VariableLengthArray.parse(data)
    print(f'parsed: {parsed}')


def variable_element_array_sample():
    pass


if __name__ == '__main__':
    tuple_sample()
    lazy_length_sample()
    variable_element_array_sample()
