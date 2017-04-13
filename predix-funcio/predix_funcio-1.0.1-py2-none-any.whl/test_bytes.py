import unittest
import bytes
import StringIO
import exception

class BytesTestCase(unittest.TestCase):
    def test_intToBytes(self):
        convertedBytes = bytes.intToBytes(0xDEADBEEF)
        expectedBytes = bytearray(b'\xef\xbe\xad\xde')
        self.assertEqual(convertedBytes, expectedBytes)

    def test_bytesToInt(self):
        inputBytes = bytearray(b'\xef\xbe\xad\xde')
        convertedInt = bytes.bytesToInt(inputBytes)
        expectedInt = 0xDEADBEEF
        self.assertEqual(convertedInt, expectedInt)

    def test_simpleReadNBytes(self):
        fileObject = StringIO.StringIO(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')
        bytesA = bytes.readNBytes(fileObject, 5)
        bytesB = bytes.readNBytes(fileObject, 5)

        expectedBytesA = bytearray(b'\x00\x01\x02\x03\x04')
        expectedBytesB = bytearray(b'\x05\x06\x07\x08\x09')

        self.assertEqual(bytesA, expectedBytesA)
        self.assertEqual(bytesB, expectedBytesB)

    def test_exceptionReadNBytes(self):
        caughtException = False
        fileObject = StringIO.StringIO(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')

        try:
            bytes.readNBytes(fileObject, 12)
        except exception.FuncioException:
            caughtException = True

        self.assertTrue(caughtException)

if __name__ == '__main__':
    unittest.main()
