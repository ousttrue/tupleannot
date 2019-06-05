import unittest
import pathlib
from tupleannot import *

HERE = pathlib.Path(__file__).resolve().parent

class BMP(Base):
    bfType: UInt16
    bfSize: UInt32
    bfReserved1: UInt16
    bfReserved2: UInt16
    bfOffBits: UInt32
    biSize: UInt32
    biWidth: UInt32
    biHeight: UInt32
    biPlanes: UInt16
    biBitCount: UInt16
    biCompression: UInt32
    biSizeImage	: UInt32
    biXPixPerMeter: UInt32
    biYPixPerMeter: UInt32
    biClrUsed: UInt32
    biCirImportant: UInt32
    pixels: UInt8[-5]



class BitmapTest(unittest.TestCase):
    def test_bmp(self):
        path = HERE / '2x2.bmp'
        data = path.read_bytes()
        parsed, remain = BMP.parse(data)
        print(parsed.value())


if __name__ == '__main__':
    unittest.main()