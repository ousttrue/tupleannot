import struct
import collections
import typing

VERSION = [0, 1, 0]


class _MetaDefinition(type):
    def __new__(metacls, name, bases, namespace, **kwds):
        annotations = namespace.get('__annotations__')
        if annotations:
            #print(f'tuple: {name}')
            element_size = 0
            for k, v in annotations.items():
                element_size += v.__element_size__

            # Create Tuple
            class TypedTuple(metaclass=_MetaDefinition):
                __element_size__ = element_size
                __tuple_items__ = annotations

                def __init__(self, segment: bytes) -> None:
                    self.segment = segment
                    self.values = []

                def __getitem__(self, key: str):
                    self._parse_values()
                    for x, (k,
                            v) in zip(self.values,
                                      self.__class__.__tuple_items__.items()):
                        if k == key:
                            return x

                def _parse_values(self):
                    if self.values:
                        return
                    it = iter(self.__class__.__tuple_items__.items())
                    src = self.segment
                    while True:
                        try:
                            _, v = next(it)
                            value, src = v.parse(src)
                            self.values.append(value.value())
                        except StopIteration:
                            break

                def value(self):
                    self._parse_values()
                    return {
                        k: x
                        for x, (
                            k,
                            v) in zip(self.values,
                                      self.__class__.__tuple_items__.items())
                    }

                @classmethod
                def parse(cls, data: bytes) -> typing.Tuple[bytes, bytes]:
                    it = iter(annotations.items())
                    src = data
                    size = 0
                    while True:
                        try:
                            _, annotation = next(it)
                            parsed, src = annotation.parse(src)
                            size += len(src)
                        except StopIteration:
                            break
                    return cls(data[0:size]), src

            return TypedTuple
        else:
            return type.__new__(metacls, name, bases, dict(namespace))

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __getitem__(self, length: int):
        '''
        create Array class by []. ex: UInt32[4]
        '''

        class Array(self):
            __element_size__ = self.__element_size__
            __length__ = length

            def __init__(self, segment: bytes) -> None:
                super().__init__(segment)

            def __getitem__(self, i: int) -> self:
                size = self.__class__.__element_size__
                pos = size * i
                cls = self.__class__.__bases__[0]
                return cls(self.segment[pos:pos +
                                        self.__class__.__element_size__])

            def value(self):
                size = self.__class__.__element_size__
                return [
                    self.__class__.__bases__[0](self.segment[x:x + size]).value()
                    for x in range(0, len(self.segment), size)
                ]

            @classmethod
            def parse(cls, src: bytes) -> typing.Tuple[bytes, bytes]:
                s = cls.__element_size__ * cls.__length__
                value = src[0:s]
                remain = src[s:]
                return cls(value), remain

        return Array


class Base(metaclass=_MetaDefinition):
    __length__ = 0

    def __init__(self, segment: bytes) -> None:
        self.segment = segment

    def value(self):
        s = self.__class__.__length__
        if s == 0:
            s = 1
        return struct.unpack(f'{s}{self.__class__.__fmt__}', self.segment)[0]

    @classmethod
    def parse(cls, src: bytes) -> typing.Tuple[bytes, bytes]:
        s = cls.__element_size__
        value = src[0:s]
        remain = src[s:]
        return cls(value), remain


class Int8(Base):
    __fmt__ = 'b'
    __element_size__ = 1


class Int16(Base):
    __fmt__ = 'h'
    __element_size__ = 2


class Int32(Base):
    __fmt__ = 'i'
    __element_size__ = 4


class Int64(Base):
    __fmt__ = 'q'
    __element_size__ = 8


class UInt8(Base):
    __fmt__ = 'B'
    __element_size__ = 1


class UInt16(Base):
    __fmt__ = 'H'
    __element_size__ = 2


class UInt32(Base):
    __fmt__ = 'I'
    __element_size__ = 4


class UInt64(Base):
    __fmt__ = 'Q'
    __element_size__ = 8


class Float(Base):
    __fmt__ = 'f'
    __element_size__ = 4


class Double(Base):
    __fmt__ = 'd'
    __element_size__ = 8


def main():
    data = struct.pack('6I', 1, 2, 3, 4, 5, 6)
    parsed, remain = UInt32.parse(data)
    print(f'UInt32: {parsed.value()}')

    parsed, remain = UInt32[2].parse(data)
    print(f'Uint32[2]: {parsed.value()}')

    class Vec3(Base):
        x: UInt32
        y: UInt32
        z: UInt32

    parsed, remain = Vec3.parse(data)
    print(f'remain: {remain}')
    print(f'vec3: {parsed.value()}')

    parsed, remain = Vec3[2].parse(data)
    print(f'parsed[0]["x"]: {parsed[0]["x"]}')


if __name__ == '__main__':
    main()