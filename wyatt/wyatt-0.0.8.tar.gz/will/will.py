import json, requests, sys, os
URL="https://iex.ist/api/message/"
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

def send(message, name="annonymous", to="will"):
    data={'text': message, 'to': to, 'sender': name}
    code=requests.post(URL, data=json.dumps(data)).status_code
    if code==201:
        print('Sent message.')
    else:
        print('Failed to send message. %s'%code)

def get(quantity=5, offset=0):
    params={'limit': quantity, 'offset': offset, 'order_by': "-id"}
    return json.loads(requests.get(URL, params=json.dumps(params)).text)['objects']

def stdout(message):
    sys.stdout.write(message)
    sys.stdout.write('\b' * len(message))
    
def display(objects):
    rows, columns = os.popen('stty size', 'r').read().split()
    for msg in objects:
        print("%s%s%s,"%(bcolors.BOLD,msg['to'],bcolors.ENDC))
        print("  %s"%msg['text'])
        print("\t\t\t%s-%s%s"%(bcolors.OKBLUE,msg['sender'], bcolors.ENDC))

