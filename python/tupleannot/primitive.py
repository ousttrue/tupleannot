import collections
import struct
from typing import NamedTuple, Any, Tuple


class ParentWithIndex(NamedTuple):
    parent: Any
    index: int


class MetaDefinition(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __getitem__(self, length: int):
        '''
        create Array class by []. ex: UInt32[4]

        ToDo: negative length(only Tuple member)
        '''

        def parse_fixed_array(cls, src: bytes, parent: ParentWithIndex) -> Tuple[Base, bytes]:
            s = cls.__element_size__ * cls.__length__
            value = src[0:s]
            remain = src[s:]
            return cls(value, parent), remain

        class Array(self):
            __element_size__ = self.__element_size__
            __length__ = length

            def __init__(self, segment: bytes,
                         parent: ParentWithIndex) -> None:
                super().__init__(segment, parent)
                self.reference = None

            def __getitem__(self, i: int) -> self:
                size = self.__class__.__element_size__
                cls = self.__class__.__bases__[0]
                begin = size * i
                end = begin + size
                return cls.parse(self.segment[begin:end], ParentWithIndex(self, i))[0]

            def value(self):
                return [self[i] for i in range(0, self.__class__.__length__)]

            @classmethod
            def parse(cls, src: bytes, parent=None) -> Tuple[Base, bytes]:
                return parse_fixed_array(cls, src, parent)

        return Array


class Base(metaclass=MetaDefinition):
    def __init__(self, segment: bytes, parent: ParentWithIndex) -> None:
        self.segment = segment
        self.parent = parent


class Primitive(Base):
    '''
    Int8, 16, 32, 64
    UInt8, 16, 32, 64
    Float, Double
    '''

    def value(self):
        return struct.unpack(f'{self.__class__.__fmt__}', self.segment)[0]

    @classmethod
    def parse(cls, src: bytes, parent=None) -> Tuple[bytes, bytes]:
        s = cls.__element_size__
        value = src[0:s]
        remain = src[s:]
        return cls(value, parent), remain


class Int8(Primitive):
    __fmt__ = 'b'
    __element_size__ = 1


class Int16(Primitive):
    __fmt__ = 'h'
    __element_size__ = 2


class Int32(Primitive):
    __fmt__ = 'i'
    __element_size__ = 4


class Int64(Primitive):
    __fmt__ = 'q'
    __element_size__ = 8


class UInt8(Primitive):
    __fmt__ = 'B'
    __element_size__ = 1


class UInt16(Primitive):
    __fmt__ = 'H'
    __element_size__ = 2


class UInt32(Primitive):
    __fmt__ = 'I'
    __element_size__ = 4


class UInt64(Primitive):
    __fmt__ = 'Q'
    __element_size__ = 8


class Float(Primitive):
    __fmt__ = 'f'
    __element_size__ = 4


class Double(Primitive):
    __fmt__ = 'd'
    __element_size__ = 8


def main():
    data = struct.pack('6I', 1, 2, 3, 4, 5, 6)
    parsed, remain = UInt32.parse(data)
    print(f'UInt32: {parsed.value()}')

    parsed, remain = UInt32[6].parse(data)
    print(f'UInt32[0]: {parsed[0].value()}')
    print(f'UInt32[5]: {parsed[5].value()}')


if __name__ == '__main__':
    main()