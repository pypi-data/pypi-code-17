# Functions for monoalpha - please read README

import string

def alphatrans(plaintext, alpha1, alpha2):
    alpha1 = alpha1.lower()
    alpha2 = alpha2.lower()
    plaintext = plaintext.lower()
    codetext = "" # Initialises the coded text to be returned.
    for char in plaintext:
        try:
            # Attempts to locate character of plaintext in alpha1,
            # and add the corresponding character of alpha2
            # to codetext.
            index = alpha1.index(char)
            codetext += alpha2[index].upper()
        except:
            # Adds original character to codetext if it cannot be encrypted.
            codetext += char
    return codetext


def encrypt(plaintext, alphabet):
    plainalpha = string.ascii_lowercase # Gets plaintext alpabet.
    return alphatrans(plaintext, plainalpha, alphabet)

def decrypt(plaintext, alphabet):
    plainalpha = string.ascii_lowercase # Gets plaintext alpabet.
    return alphatrans(plaintext, alphabet, plainalpha)


def caesar(offset):
    offset = int(offset)
    plainalpha = string.ascii_lowercase
    codealpha = "" # Initialises the coded alphabet to be returned.
    for i in range(26):
        # Adds offset to index, and then applies modulo
        # to keep within the range of the alphabet.
        index = (i+offset)%26
        codealpha += plainalpha[index]
    return codealpha

def rot13():
    return caesar(13)

def affine(a, b):
    a = int(a)
    b = int(b)
    plainalpha = string.ascii_lowercase
    codealpha = "" # Initialises the coded alphabet to be returned.
    for i in range(26):
        index = ((a*i)+b)%26 # Applies the affine formula to the index.
        codealpha += plainalpha[index]
    return codealpha

def atbash():
    # Atbash is the same as affine where a = 25 and b = 25.
    return affine(25, 25)

def keyword(word):
    plainalpha = string.ascii_lowercase
    word = word.lower()
    codealpha = ""
    for char in word:
        if char in plainalpha:
            codealpha += char
            # Removes character so it will not be repeated.
            plainalpha = plainalpha.replace(char, "")
    for char in plainalpha:
        codealpha += char # Adds remainder of alphabet.
    return codealpha


def caesar_encrypt(plaintext, offset):
    return encrypt(plaintext, caesar(offset))

def caesar_decrypt(plaintext, offset):
    return decrypt(plaintext, caesar(offset))

def rot13_encrypt(plaintext):
    return encrypt(plaintext, rot13())

def rot13_decrypt(plaintext):
    return decrypt(plaintext, rot13())

def affine_encrypt(plaintext, a, b):
    return encrypt(plaintext, affine(a, b))

def affine_decrypt(plaintext, a, b):
    return decrypt(plaintext, affine(a, b))

def atbash_encrypt(plaintext):
    return encrypt(plaintext, atbash())

def atbash_decrypt(plaintext):
    return decrypt(plaintext, atbash())

def keyword_encrypt(plaintext, word):
    return encrypt(plaintext, keyword(word))

def keyword_decrypt(plaintext, word):
    return decrypt(plaintext, keyword(word))
