import unittest
import pathlib
from tupleannot import *

HERE = pathlib.Path(__file__).resolve().parent

bmp = Tuple('bmp', [
    UInt16('bfType'),
    UInt32('bfSize'),
    UInt16('bfReserved1'),
    UInt16('bfReserved2'),
    UInt32('bfOffBits'),
    UInt32('biSize'),
    UInt32('biWidth'),
    UInt32('biHeight'),
    UInt16('biPlanes'),
    UInt16('biBitCount'),
    UInt32('biCompression'),
    UInt32('biSizeImage	'),
    UInt32('biXPixPerMeter'),
    UInt32('biYPixPerMeter'),
    UInt32('biClrUsed'),
    UInt32('biCirImportant'),
    UInt8('pixels', -5)
])


class BitmapTest(unittest.TestCase):
    def test_bmp(self):
        path = HERE / '2x2.bmp'
        data = path.read_bytes()
        bmp.parse(data)
        print(bmp)


if __name__ == '__main__':
    unittest.main()