import collections
import struct
from typing import NamedTuple, Any, Tuple


class ParentWithIndex(NamedTuple):
    value: Any
    index: int


class MetaDefinition(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __getitem__(cls, length_or_offset: int):
        '''
        create Array class by []. ex: UInt32[4]
        '''

        if length_or_offset < 0:
            # lazy length. determine array length by other value
            offset = length_or_offset

            def get_length(parent):
                return parent.value[parent.index + offset].value()
        else:
            length = length_or_offset

            def get_length(_):
                return length

        class Array(cls):
            __element_size__ = cls.__element_size__
            __get_length__ = get_length

            def __init__(self,
                         segment: bytes,
                         parent: ParentWithIndex,
                         values=None) -> None:
                super().__init__(segment, parent)
                self.values = values

            def __str__(self) -> str:
                return f'[{", ".join(str(x) for x in self.value())}]'

            def __getitem__(self, i: int) -> cls:
                if self.values:
                    # variable element length. already parsed
                    return self.values[i]
                else:
                    size = self.__class__.__element_size__
                    base_cls = self.__class__.__bases__[0]
                    begin = size * i
                    end = begin + size
                    return base_cls.parse(self.segment[begin:end],
                                          ParentWithIndex(self, i))[0]

            def value(self):
                return [
                    self[i] for i in range(
                        0, self.__class__.__get_length__(self.parent))
                ]

            @classmethod
            def is_lazy_array(cls):
                return length_or_offset < 0

            @classmethod
            def parse(cls, data: bytes, parent=None) -> Tuple[Base, bytes]:
                length = cls.__get_length__(parent)
                if cls.has_lazy_array():
                    values = []
                    size = 0
                    src = data
                    base_cls = cls.__bases__[0]
                    for _ in range(length):
                        value, src = base_cls.parse(src)
                        size += len(value.segment)
                        values.append(value)
                    return cls(data[0:size], parent, values), src
                else:
                    s = cls.__element_size__ * length
                    value = data[0:s]
                    remain = data[s:]
                    return cls(value, parent), remain

        return Array


class Base(metaclass=MetaDefinition):
    def __init__(self, segment: bytes, parent: ParentWithIndex) -> None:
        self.segment = segment
        if parent:
            if not isinstance(parent, ParentWithIndex):
                raise Exception('invalid parent')
        self.parent = parent

    @classmethod
    def has_lazy_array(cls):
        return False

    @classmethod
    def is_lazy_array(cls):
        return False

    @classmethod
    def is_tuple(cls):
        return False


class Primitive(Base):
    '''
    Int8, 16, 32, 64
    UInt8, 16, 32, 64
    Float, Double
    '''

    def __str__(self)->str:
        return str(self.value())

    def value(self):
        return struct.unpack(f'{self.__class__.__fmt__}', self.segment)[0]

    @classmethod
    def parse(cls, src: bytes, parent=None) -> Tuple[bytes, bytes]:
        s = cls.__element_size__
        value = src[0:s]
        remain = src[s:]
        return cls(value, parent), remain


class Int8LE(Primitive):
    __fmt__ = '<b'
    __element_size__ = 1


class Int16LE(Primitive):
    __fmt__ = '<h'
    __element_size__ = 2


class Int32LE(Primitive):
    __fmt__ = '<i'
    __element_size__ = 4


class Int64LE(Primitive):
    __fmt__ = '<q'
    __element_size__ = 8


class UInt8LE(Primitive):
    __fmt__ = '<B'
    __element_size__ = 1


class UInt16LE(Primitive):
    __fmt__ = '<H'
    __element_size__ = 2


class UInt32LE(Primitive):
    __fmt__ = '<I'
    __element_size__ = 4


class UInt64LE(Primitive):
    __fmt__ = '<Q'
    __element_size__ = 8


class FloatLE(Primitive):
    __fmt__ = '<f'
    __element_size__ = 4


class DoubleLE(Primitive):
    __fmt__ = '<d'
    __element_size__ = 8


def main():
    data = struct.pack('6I', 1, 2, 3, 4, 5, 6)
    parsed, remain = UInt32LE.parse(data)
    print(f'UInt32: {parsed.value()}')

    parsed, remain = UInt32LE[6].parse(data)
    print(f'UInt32[0]: {parsed[0].value()}')
    print(f'UInt32[5]: {parsed[5].value()}')


if __name__ == '__main__':
    main()