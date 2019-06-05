import struct
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Any, List

VERSION = [0, 0, 1]


class ElementType:
    Fixed = 0
    Variable = 0


class Definition(metaclass=ABCMeta):
    '''
    ElementSize x ElementCount
    '''

    def __init__(self, name: str, element_fixed_count: int,
                 element_type: ElementType) -> None:
        '''
        Parameters
        ----------
        name: str
            value name

        element_fixed_count: int
            if > 0: element count. value is array
            if == 0: value is single value 
            if < 0: index offset for value count sotore
        
        element_type: ArrayElement, default Fixed
            if Variable: value in this array has variable length size
        '''
        self.name = name
        self.element_count_reference = None
        if element_fixed_count < 0:
            # ref
            self.element_fixed_count = element_fixed_count
        else:
            # fixed array
            self.element_fixed_count = element_fixed_count
        self.segment = bytes()
        self.element_type = element_type

    def __getitem__(self, i: int):
        if self.element_fixed_count == 0:
            raise IndexError('not array')
        else:
            raise NotImplementedError()

    def element_count(self) -> int:
        '''
        element count in this array
        '''
        if self.element_fixed_count < 0:
            return self.element_count_reference.value()
        elif self.element_fixed_count == 0:
            return 1
        else:
            return self.element_fixed_count

    def __str__(self) -> None:
        if self.element_fixed_count == 0:
            return str(self.element_value())
        else:
            element_count = self.element_count()
            return f'{self.name}[{element_count}]'

    def value(self):
        if self.element_fixed_count == 0:
            # single value
            return self.element_value()
        else:
            return [self[i] for i in range(self.element_count())]

    def parse(self, src: bytes) -> bytes:
        '''
        consume data and return remain
        '''
        element_count = self.element_count()
        if element_count == 1:
            return self.parse_element(src)
        elif self.element_type == ElementType.Variable:
            for _ in range(element_count):
                src = self.parse_element(src)
            return src
        else:
            s = element_count * self.element_size()
            self.segment = src[0:s]
            return src[s:]

    @abstractmethod
    def parse_element(self, src: bytes) -> bytes:
        pass

    @abstractmethod
    def element_size(self) -> int:
        pass

    @abstractmethod
    def element_value(self) -> Any:
        pass


class Primitive(Definition):
    '''
    https://docs.python.org/3/library/struct.html
    '''

    def __init__(self, name, element_count, fmt, element_size):
        super().__init__(name, element_count, False)
        self.fmt = fmt
        self.size = element_size

    def parse_element(self, src: bytes) -> bytes:
        self.segment = src[0:self.size]
        return src[self.size:]

    def element_size(self) -> int:
        return self.size

    def element_value(self) -> Any:
        return struct.unpack(self.fmt, self.segment)[0]


class Int8(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'b', 1)


class Int16(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'h', 2)


class Int32(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'i', 4)


class Int64(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'q', 8)


class UInt8(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'B', 1)


class UInt16(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'H', 2)


class UInt32(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'I', 4)


class UInt64(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'Q', 8)


class Float(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'f', 4)


class Double(Primitive):
    def __init__(self, name, element_count=0) -> None:
        super().__init__(name, element_count, 'd', 8)


class String(UInt8):
    def __init__(self, name: str, element_fixed_count: int,
                 encoding='utf-8') -> None:
        super().__init__(name, element_fixed_count)
        self.encoding = encoding

    def __str__(self) -> None:
        return self.element_value()

    def element_value(self):
        if self.segment:
            try:
                end = self.segment.index(b'\0')
                return self.segment[0:end].decode(self.encoding)
            except ValueError:
                return self.segment.decode(self.encoding)
        else:
            return ''


class Tuple(Definition):
    def __init__(self,
                 name: str,
                 parsers: List[Definition],
                 element_fixed_count=0,
                 element_type=ElementType.Fixed) -> None:
        super().__init__(name, element_fixed_count, element_type)
        self.parsers = parsers
        for i, p in enumerate(self.parsers):
            if p.element_fixed_count < 0:
                p.element_count_reference = parsers[i + p.element_fixed_count]

    def __getitem__(self, key: Any):
        if isinstance(key, str):
            parser = next(x for x in self.parsers if x.name == key)
            if isinstance(parser, Tuple):
                return parser
            else:
                return parser.value()
        else:
            return super()[key]

    def __str__(self) -> None:
        if self.element_count() == 1:
            return f'{[str(x) for x in self.parsers]}'
        else:
            return super().__str__()

    def parse_element(self, src: bytes) -> bytes:
        it = iter(self.parsers)
        while True:
            try:
                p = next(it)
                src = p.parse(src)
            except StopIteration:
                break
        return src

    def element_size(self):
        return sum(p.element_size() * p.element_count() for p in self.parsers)

    def element_value(self):
        return [x.value() for x in self.parsers]
