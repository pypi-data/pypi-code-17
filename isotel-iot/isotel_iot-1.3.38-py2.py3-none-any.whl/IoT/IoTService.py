"""
Service API utilites

Contains static utility functions and basic service implementation
"""
import json
from socket import *

import time
import sys
from isotel.IoT import IoT 
import select
from enum import Enum, unique


def flush_print(str):
    print(str)
    sys.stdout.flush()
    return


def parse_message(message):
    """
    Parses raw message into dictionary
    
    Keys:
    - keyword: message keyword
    - action: action to be performed, if present
    - uri: message uri
    - body: message body
    """
    data = {} 
    
    if message.endswith("\n\n"):
        message = message[:-2]
        split = message.partition(' ')
        data["keyword"] = split[0]
        if data["keyword"] == "PING":
            data["action"] = "ping"
        else:    
            if '\r\n' in split[2]:
                split = split[2].partition('\r\n')
                data["uri"] = split[0]  

                try:                
                    body = json.loads(split[2])
                    data["body"] = body
                    if "action" in body:                    
                        data["action"] = body["action"]
                except:
                    data["body"] = split[2]
            else:
                data["uri"] = split[2]      
            
    return data


def encode_message(msg=None, uri=None, keyword="REPLY"):
    """
    Encode reply to a message
    
    Default keyword is REPLY unless specified otherwise
    """
    data = keyword + " "
    
    
    if uri:
        data += str(uri)
    if msg:
        data += "\r\n" if uri else ""
        data += str(msg)
    
    data += "\n\n"
    return data


def encode_http_reply(body, status=200, mimetype=None, headers=None):
    """
    encode http format reply

    :param body: reply body
    :param status: HTTP status status code
    :param mimetype: reply mimetype
    :param headers: optionl header entries
    :return:
    """
    data = {'body': body, 'status':status}
    if mimetype:
        data['mime'] = mimetype
    if headers:
        data['headers'] = headers
    return encode_message(msg=json.dumps(data), uri=None, keyword='HREPLY')


def encode_notification(module, msg, severity="API", receiver=None):
    """
    Encode notification message
    """
    data = {"module":module, "message":msg, "severity":severity}
    if receiver:
        data["receiver"] = receiver
    return encode_message(msg=json.dumps(data), uri=None, keyword="NOTIFY")


def encode_connect_request(device, debounce_time=1000, send_data=True):
    """
    Encode device or parameter connection request
    """
    uri = "me/" + device.replace('.', '/')
    body = {"send_data" : send_data, "debounce_time": debounce_time}
    return encode_message(msg=json.dumps(body), uri=uri, keyword="CONNECT")


def encode_disconnect_request(device):
    """
    Encode device or parameter disconnection request
    """
    uri = "me/" + device.replace('.', '/')
    return encode_message(msg=None, uri=uri, keyword="DISCONNECT")

@unique
class RStatus(Enum):
    """
    HTTP Status responses
    """
    OK = 200,
    NO_CONTENT = 204,
    PARTIAL_CONTENT = 206,
    MULTI_STATUS = 207,
    REDIRECT = 301,
    REDIRECT_SEE_OTHER = 303,
    NOT_MODIFIED = 304,
    BAD_REQUEST = 400,
    UNAUTHORIZED = 401,
    FORBIDDEN = 403,
    NOT_FOUND = 404,
    METHOD_NOT_ALLOWED = 405,
    NOT_ACCEPTABLE = 406,
    REQUEST_TIMEOUT = 408,
    CONFLICT = 409,
    RANGE_NOT_SATISFIABLE = 416,
    UNPROCESSABLE_ENTITY = 422,
    INTERNAL_ERROR = 500,
    NOT_IMPLEMENTED = 501,
    UNSUPPORTED_HTTP_VERSION = 505

@unique
class Mime(Enum):
    """
    HTTP mime types
    """

    MIME_PLAINTEXT = "text/plain",
    MIME_HTML = "text/html",
    MIME_JSON = "application/json";

class BasicService():
    """
    Basic service implementation running in single thread
    """
    
    def __init__(self, host, port, http_group, service_name, check_pin=False):
        """
        
        """
        self.host = host
        self.port = int(port)
        self.http_group = http_group
        self.name = service_name
        self.connected = False
        
        if check_pin:
            auth = self.http_group.get_service_pin(self.name)
            self.pin = auth["pin"]
        else:
            self.pin = None
    """       
    def setIdent(self, name, version, vendor):
        self.ident = {}
        self.ident["name"] = name
        self.ident["version"] = version
        self.ident["vendor"] = vendor
        if self.pin:
            data["pin"] = self.pin
    """

    def get_ident(self):
        """
        Get identification (IDENT) data
        
        Override to specify custom data
                
        """
        data = {}
        data["name"] = self.name
        data["version"] = self.version
        data["vendor"] = self.vendor
        
        if self.pin:
            data["pin"] = self.pin
        return  data
    
    def run_after_connecting(self):
        """
        Override to perform custom initiation before connecting to TCP server
        """
        return
    
    def run_in_loop(self):
        """
        Override to perform any custom routines in main loop after handling received messages
        """
        
        return
    
    def run_before_finish(self):
        """
        Override to perform custom routine before finishing service
        """
        return
    
    def process_received_message(self, decoded_message):
        """
        Implement custom functionality
        """
        return
    
    def process_action(self, decoded_message, raw_message):
        """
        Generate response for action type system requests of types:
        - PING
        - STOP
        - IDENT
        """
        action = decoded_message['action']
        if action == 'ping':
            return raw_message
        elif action == 'ident':
            return encode_message(msg=json.dumps(self.get_ident()), uri=None, keyword="IDENT")
        elif action == 'stop':
            return encode_message(keyword="STOP")
        else:
            return None
        
    def ping_existing(self):
        service_name = self.name
        try:
            slist = self.http_group.get_service_list()
            
            for s in slist:
                name = s["name"]
                if name is not None and name == service_name:                    
                   
                    service = IoT.Service( self.http_group, service_name)                   
                    res = service.get_service_data("?action=ping")
                    flush_print("ping response: " + str(res))
                    return True
                
        except Exception as e:
            return False  
    
    def send_data(self, data, attempt_reconnect=False):
        """
        Send data to server
        
        :param data: data to be send
        :param attempt_reconnect: attempt socket reconnection on error
        :return: 
        """
        if self.connected:
            try:
                self.tcp_socket.send(bytes(data, 'UTF-8'))
            except (OSError, BrokenPipeError)  as e:
                self.connected = False
                flush_print("Error while sending data: " + str(e))
                #if attempt_reconnect:
                #    flush_print("reconnect attempt: " )


#flushPrint("sending: " + str(data))
        
    def run_service(self, interval=5, verbose=False):
        """
        Connect to TCP server and start main service loop
        """
        
        BUFSIZ = 4096
        ADDR = (self.host, self.port)
        
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)

        self.tcp_socket.connect(ADDR)
        
        flush_print("Service connected to " + self.host )
        self.connected =True
        
        ident = encode_message(msg=json.dumps(self.get_ident()), uri=None, keyword="IDENT")
        #self.tcp_socket.send(bytes(ident, 'UTF-8'))
        self.send_data(ident)
        time.sleep(.20)
        
        #Override
        self.run_after_connecting()
            
        self.tcp_socket.setblocking(0)
        
        while True:

            if self.connected:
                ready = select.select([self.tcp_socket], [], [], interval)

                #Process received data
                if ready[0]:
                    data = self.tcp_socket.recv(BUFSIZ)

                    inp = data.decode('utf-8')

                    if verbose:
                        flush_print(inp)
                    #response = self.processData(inp)
                    parsed = parse_message(inp)

                    if "action" in parsed:
                        response = self.process_action(parsed, inp)
                    else:
                        response = self.process_received_message(parsed) #Override

                    if response is not None:
                        #self.tcp_socket.send(bytes(response, 'UTF-8'))
                        self.send_data(response)
                        if response.find("STOP") != -1:
                            break
            else:
                break
                #time.sleep(interval)

            self.run_in_loop() #Override           
                  
        
        self.tcp_socket.close()
        self.connected =False
        self.run_before_finish() #override for custom behavior
        
    
    
    