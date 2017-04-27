from time import sleep

from monitoring.monitor import wire, expose, monitorState
from test.framework.monitortestdata import ComplexObj


def startServer():
    complexDict = {
                      'key1': 'value1',
                      'key2': {
                          'subkey1': 'subvalue1',
                          'subkey2': 'subvalue2'
                      },
                      'key3': [{
                          'listsubkey1': 'listsubvalue1',
                      }, {
                          'listsubkey2': 'listsubvalue2',
                          'listsubkey3': 'listsubvalue3'
                      }]
                  }
    
    wire('complexDict', complexDict)
    wire('complexObj', ComplexObj())
    expose(port = 1234)
    
    while not monitorState['exitRequested']:
        sleep(1)


if __name__ == '__main__':
    startServer()