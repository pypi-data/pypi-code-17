# Command line for monoalpha - please read README

from .main import *
import cmd
import shlex
class CipherPrompt(cmd.Cmd):
    intro = """Welcome to monoalpha, a simple monoalphabetic cipher program
Type help or ? for more information"""
    prompt = "(monoalpha)"
    def execute(self, command, args, argnum):
        args = (shlex.split(args))
        if len(args) == argnum:
            try:
                print(command(*args))
            except:
                print("*** an error occured: please check input")
        else:
            print("*** invalid number of arguments")

    def do_alphatrans(self, args):
        "Encrypts/decrypts based on [alphabet one] and [alphabet two]."
        self.execute(alphatrans, args, 2)
        
    def do_encrypt(self, args):
        "Encrypts [plaintext] using a [code alphabet]."
        self.execute(encrypt, args, 2)

    def do_decrypt(self, args):
        "Decrypts [plaintext] using a [code alphabet]."
        self.execute(decrypt, args, 2)
        
    def do_caesar(self, args):
        "Gives caesar shift code alphabet based on [offset]."
        self.execute(caesar, args, 1)

    def do_rot13(self, args):
        "Gives code alphabet for ROT13 cipher."
        self.execute(rot13, args, 0)

    def do_affine(self, args):
        "Gives code alphabet for affine cipher based on values [a] and [b]."
        self.execute(encrypt, args, 1)

    def do_atbash(self, args):
        "Gives code alphabet for atbash cipher."
        self.execute(atbash, args, 0)
        
    def do_keyword(self, args):
        "Gives keyword code alphabet based on [keyword]."
        self.execute(keyword, args, 1)

    def do_caesar_encrypt(self, args):
        "Applies caesar shift to [plaintext] using [offset]."
        self.execute(caesar_encrypt, args, 2)

    def do_caesar_decrypt(self, args):
        "Reverses caeser shift on [coded text] using [offset]."
        self.execute(caesar_decrypt, args, 2)

    def do_rot13_encrypt(self, args):
        "Applies ROT13 cipher to [plaintext]."
        self.execute(rot13_encrypt, args, 1)
        
    def do_rot13_decrypt(self, args):
        "Decrypts ROT13 cipher on [coded text]."
        self.execute(rot13_decrypt, args, 1)

    def do_affine_encrypt(self, args):
        "Applies affine cipher to [plaintext] using values [a] and [b]."
        self.execute(affine_encrypt, args, 2)

    def do_affine_decrypt(self, args):
        "Reverses affine cipher on [plaintext] using values [a] and [b]."
        self.execute(affine_decrypt, args, 2)

    def do_atbash_encrypt(self, args):
        "Applies atbash cipher to [plaintext]."
        self.execute(atbash_encrypt, args, 1)
        
    def do_atbash_decrypt(self, args):
        "Reverses atbash cipher on [plaintext]."
        self.execute(do_atbash_decrypt, args, 1)

    def do_keyword_encrypt(self, args):
        "Applies keyword cipher to [plaintext] using [keyword]."
        self.execute(keyword_encrypt, args, 2)

    def do_keyword_decrypt(self, args):
        "Reverses keyword cipher on [plaintext] using [keyword]."
        self.execute(keyword_decrypt, args, 2)
def runcmd():
    cmdline = CipherPrompt()
    cmdline.cmdloop()
