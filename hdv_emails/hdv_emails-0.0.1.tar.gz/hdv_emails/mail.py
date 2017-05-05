from abc import ABCMeta, abstractmethod
import emails

class SMTPAbstract(metaclass=ABCMeta):
    
    def __init__(self, *args, **kargs):
        self.smtp = {}
        self.preset()
        self.build_smtp(args, kargs)
        
    def build_smtp(self, args, kargs):
        if args is not ():
            self.smtp['user'] = args[0]
            try:
                self.smtp['password'] = args[1]
            except IndexError:
                pass
        
        self.smtp.update({k:v for k, v in kargs.items()})
        
        keys_to_remove = ('__class__', 'self', 'kargs', 'args', 'smtp')
        self.smtp.update({k:v for k, v in self.__dict__.items() if k not in keys_to_remove})
        
    def send(self, message):
        r = message.send(smtp=self.smtp)
        return r
    
    @abstractmethod
    def preset(self):
        pass

class SMTP(SMTPAbstract):
    
    def prest(self):
        pass
    
class GMailSMTP(SMTP):
    
    def preset(self):
        self.host = 'smtp.gmail.com'
        self.port = 587
        self.tls = True
        
class AmazonSMTP(SMTP):
    
    def preset(self):
        self.host = 'email-smtp.us-west-2.amazonaws.com'
        self.port = 587
        self.tls = True

class Message():
    
    def __new__(cls, *args, **kargs):
        obj = emails.html(**kargs)
        return obj
