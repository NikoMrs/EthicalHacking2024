#!/usr/bin/env python3
import os
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "r") as f:
        FLAG = f.read().strip()
else:
    FLAG = "UniTN{placeholder_flag}"


BLOCK_SIZE = 16
KEY = os.urandom(BLOCK_SIZE)
ALLOWED_CHARACTERS = string.ascii_letters + " .,;?!'\""

def sanitize(s):
    for c in s:
        if c not in ALLOWED_CHARACTERS:
            print(f"Only these characters are allowed: {ALLOWED_CHARACTERS}")
            return False
    if "admin" in s:
        print("You can't be admin")
        return False
    return True

def signup():
    print("Choose a username")
    username = input("> ")
    print("Insert a description of yourself")
    description = input("> ")

    if not sanitize(username) or not sanitize(description):
        return

    token = f"desc={description}&user={username}".encode()
    padded_token = pad(token, BLOCK_SIZE)

    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
    enc_token = cipher.encrypt(padded_token)
    print("Here's your token (hex):", iv.hex() + enc_token.hex())

def login():
    try:
        print("Insert the token (hex)")
        iv_enc_token = bytes.fromhex(input("> "))
        iv, enc_token = iv_enc_token[:BLOCK_SIZE], iv_enc_token[BLOCK_SIZE:]
        cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
        padded_token = cipher.decrypt(enc_token)
        token = unpad(padded_token, BLOCK_SIZE)

        parts = token.split(b"&")
        username = None
        description = None
        for part in parts:
            pieces = part.split(b"=")
            if pieces[0] == b"user":
                username = pieces[1]
            if pieces[0] == b"desc":
                description = pieces[1]

        if username == b"admin" and description == b"I am a boss":
            print(FLAG)
        else:
            print("Welcome back", username.decode())
    except (ValueError, IndexError):
        print("Nope")

print("This is a Proof of Concept program for AESWT,")
print("a successor to JWT that aims to be faster.")
print("Let me know if you end up using it for your website authentication!")
while True:
    print()
    print("What do you want to do?")
    print("1. Create a new token")
    print("2. Login with a token")
    option = input("> ")

    if option == "1":
        signup()
    elif option == "2":
        login()
    else:
        print("Bye!")
        break
