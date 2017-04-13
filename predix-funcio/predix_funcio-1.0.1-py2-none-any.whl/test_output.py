import unittest
import output
import message
import StringIO

class OutputTestCase(unittest.TestCase):
    def test_responseSerde(self):
        headers = {"headersA": ["valueA1", "valueA2"]}
        body = bytearray("hello world", "utf-8")

        myMessage = message.Message(headers, body)
        statusCode = 200
        status = "Status OK"

        response = message.Response(statusCode, status, myMessage)
        serializedResponse = output.serializeResponse(response)
        deserializedResponse = output.deserializeResponse(StringIO.StringIO(serializedResponse))

        self.assertEqual(response, deserializedResponse)

    def test_simpleMultiMessageFuncWriterTest(self):
        headersA = {"headersA": ["valueA1", "valueA2"]}
        bodyA = bytearray("hello world", "utf-8")

        myMessageA = message.Message(headersA, bodyA)

        statusCodeA = 201
        statusA = "My status A"

        responseA = message.Response(statusCodeA, statusA, myMessageA)

        headersB = {"headersB": ["valueB1", "valueB2"]}
        bodyB = bytearray("hello world asdjfksajd", "utf-8")

        myMessageB = message.Message(headersB, bodyB)

        statusCodeB = 202
        statusB = "My status B"

        responseB = message.Response(statusCodeB, statusB, myMessageB)

        fileobject = StringIO.StringIO()
        funcWriter = output.FuncWriter(fileobject)

        funcWriter.writeMessage(responseA)
        funcWriter.writeMessage(responseB)

        writtenBytes = fileobject.getvalue()
        resuleFileObject = StringIO.StringIO(writtenBytes)

        deserializedResponseA = output.deserializeResponse(resuleFileObject)
        deserializedResponseB = output.deserializeResponse(resuleFileObject)

        self.assertEqual(responseA, deserializedResponseA)
        self.assertEqual(responseB, deserializedResponseB)

if __name__ == '__main__':
    unittest.main()
