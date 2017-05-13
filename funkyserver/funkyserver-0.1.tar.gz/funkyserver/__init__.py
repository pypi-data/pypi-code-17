#Used for the wesberver
from flask import Flask

#Used to create the process in which our server will reside
from multiprocessing import Process

#Used to load a browser window at localhost:port upon starting the server
import webbrowser

class FunkyServer(object):
    app = None
    process = None
    host = 'localhost'
    port = 5000

    #Constructor
    def __init__(self):
        self.app = Flask('app')

    #Add an endpoint for the server, so that the server can return data via the handler function
    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None):
        self.app.add_url_rule(endpoint, endpoint_name, handler)

    #This is the process that will run the server in the background
    def create_process(self):
        self.app.run(host=self.host, port=self.port)

    #Start the process
    #If open_new_window is True, open localhost:port in a new window
    def start(self, open_new_window=True):
        self.process = Process(target=self.create_process)
        self.process.start()

        if open_new_window:
            webbrowser.open("%s:%s" % (self.host, self.port))

    #Stop the process
    def stop(self):
        self.process.terminate()
        self.process.join()

    #Getters
    def get_port(self):
        return self.port

    def get_host(self):
        return self.host
    
    #Setters
    def set_port(self, port):
        self.port = port

    def set_host(self, host):
        self.host = host
