import unittest
import pathlib
from tupleannot import *

HERE = pathlib.Path(__file__).resolve().parent

class BMP(TypedTuple):
    bfType: UInt16LE
    bfSize: UInt32LE
    bfReserved1: UInt16LE
    bfReserved2: UInt16LE
    bfOffBits: UInt32LE
    biSize: UInt32LE
    biWidth: UInt32LE
    biHeight: UInt32LE
    biPlanes: UInt16LE
    biBitCount: UInt16LE
    biCompression: UInt32LE
    biSizeImage	: UInt32LE
    biXPixPerMeter: UInt32LE
    biYPixPerMeter: UInt32LE
    biClrUsed: UInt32LE
    biCirImportant: UInt32LE
    pixels: UInt8LE[-5]



class BitmapTest(unittest.TestCase):
    def test_bmp(self):
        path = HERE / '2x2.bmp'
        data = path.read_bytes()
        parsed, remain = BMP.parse(data)
        print(parsed.value())


if __name__ == '__main__':
    unittest.main()