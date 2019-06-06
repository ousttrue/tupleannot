import collections
from typing import Tuple, Any
try:
    from .primitive import *
except ImportError:
    from primitive import *


class MetaString(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __getitem__(cls, length_or_offset):
        '''
        ex: String[20, 'cp932']
        '''

        if isinstance(length_or_offset, tuple):
            encoding = length_or_offset[1]
            length_or_offset = length_or_offset[0]
        else:
            encoding = 'utf-8' # default



        if isinstance(length_or_offset, str):
            # lazy length. determine array length by other value
            key = length_or_offset

            def get_length(parent):
                return parent.value[key].value()

        elif length_or_offset < 0:
            offset = length_or_offset

            def get_length(parent):
                return parent.value[parent.index + offset].value()

        else:
            length = length_or_offset

            def get_length(_):
                return length

        class Array(UInt8):
            __get_length__ = get_length

            def __init__(self,
                         segment: bytes,
                         parent: ParentWithIndex,
                         encoding) -> None:
                super().__init__(segment, parent)
                self.encoding=encoding

            def __str__(self) -> str:
                return f'"{self.value()}"'

            def value(self):
                try:
                    end = self.segment.index(0)
                except ValueError:
                    end = len(self.segment)
                return self.segment[:end].decode(self.encoding)

            @classmethod
            def value_size(cls):
                if cls.is_lazy_array():
                    raise Exception('lazy array not has value_size')
                return length_or_offset

            @classmethod
            def is_lazy_array(cls):
                return length_or_offset < 0

            @classmethod
            def parse(cls, data: bytes, parent=None) -> Tuple[Any, bytes]:
                length = cls.__get_length__(parent)
                s = cls.__element_size__ * length
                value = data[0:s]
                remain = data[s:]
                return cls(value, parent, encoding), remain

        return Array

    
class String(metaclass=MetaString): pass


def string_sample():
    data = '文字列utf-8'.encode('utf-8')
    parsed, remain = String[14].parse(data)
    print(parsed)

    data = '文字列cp932'.encode('cp932')
    parsed, remain = String[11, 'cp932'].parse(data)
    print(parsed)

if __name__ == '__main__':
    string_sample()
