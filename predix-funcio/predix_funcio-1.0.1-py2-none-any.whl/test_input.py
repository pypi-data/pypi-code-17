import unittest
import input
import message
import StringIO

class InputTestCase(unittest.TestCase):
    def test_multiMessageFuncReader(self):
        headersA = {"headersA": ["valueA1", "valueA2"]}
        bodyA = bytearray("hello world", "utf-8")

        myMessageA = message.Message(headersA, bodyA)
        myMessageBytesA = input.serializeMessage(myMessageA)

        headersB = {"headersB": ["valueB1", "valueB2"]}
        bodyB = bytearray("hello world asdjfksajd", "utf-8")

        myMessageB = message.Message(headersB, bodyB)
        myMessageBytesB = input.serializeMessage(myMessageB)

        myMessageBytesA.extend(myMessageBytesB)
        fileobject = StringIO.StringIO(myMessageBytesA)

        funcReader = input.FuncReader(fileobject)
        readMessage1 = funcReader.nextMessage()
        readMessage2 = funcReader.nextMessage()

        self.assertEqual(myMessageA, readMessage1)
        self.assertEqual(myMessageB, readMessage2)

    def test_headersSerdeTest(self):
        headers = {"headersA": ["valueA1", "valueA2"],
                   "headersB": ["valueB1"],
                   "headersC": ["valueC1", "valueC2"]}

        serializedHeaders = input.serializeHeaders(headers)
        deserializedHeaders = input.deserializeHeaders(serializedHeaders)

        self.assertEqual(headers, deserializedHeaders)

    def test_serdeMessage(self):
        headers = {"headersA": ["valueA1", "valueA2"]}
        body = bytearray("hello world", "utf-8")

        myMessage = message.Message(headers, body)
        myMessageBytes = input.serializeMessage(myMessage)

        self.assertTrue(len(myMessageBytes) > 1)

        fileobject = StringIO.StringIO(myMessageBytes)
        deserializedMessage = input.deserializeMessage(fileobject)

        self.assertEqual(myMessage, deserializedMessage)

    def test_serdeMessageWithBinaryBody(self):
        headers = {"headersA": ["valueA1", "valueA2"]}
        body = bytearray(b'\xde\xad\xbe\xef\x00\xff')

        myMessage = message.Message(headers, body)
        myMessageBytes = input.serializeMessage(myMessage)

        self.assertTrue(len(myMessageBytes) > 1)

        fileobject = StringIO.StringIO(myMessageBytes)
        deserializedMessage = input.deserializeMessage(fileobject)

        self.assertEqual(myMessage, deserializedMessage)

if __name__ == '__main__':
    unittest.main()
