#!/usr/bin/env python3
from Crypto.Util.number import isPrime, long_to_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from hashlib import sha256
from random import randint
import traceback
import os

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


BLOCK_SIZE = 16
p = 2410312426921032588552076022197566074856950548502459942654116941958108831682612228890093858261341614673227141477904012196503648957050582631942730706805009223062734745341073406696246014589361659774041027169249453200378729434170325843778659198143763193776859869524088940195577346119843545301547043747207749969763750084308926339295559968882457872412993810129130294592999947926365264059284647209730384947211681434464714438488520940127459844288859336526896320919633919
g = 2

assert isPrime(p)


def bye():
    print(traceback.format_stack()[2])
    print("Oh no, they spotted you!")
    exit(0)

def input_ga_gb(prompt):
    try:
        ga_gb = int(input(prompt))
    except ValueError:
        bye()
    if ga_gb < 2 or ga_gb > p-1:
        bye()
    return ga_gb

def input_encrypted_message(cipher, expected, prompt):
    try:
        message = unpad(cipher.decrypt(bytes.fromhex(input(prompt))), BLOCK_SIZE)
    except ValueError:
        bye()
    if message != expected:
        bye()


print("Welcome to the Very Simplified Man In The Middle Simulator!")
print("You are doing a MITM attack against Alice and Bob. The messages you intercept will be prompted as 'Intercepted from <name>: <message>' and the ones you want to send will be asked as 'Send to <name>: '")
print("Try to sniff all the messages Alice and Bob are exchanging. The parameters used are")
print(p)
print(g)

a = randint(1, p-1)
ga = pow(g, a, p)
print("Intercepted from Alice:", ga)
ga_attacker = input_ga_gb("Send to Bob: ")

b = randint(1, p-1)
gb = pow(g, b, p)
print("Intercepted from Bob:", gb)
gb_attacker = input_ga_gb("Send to Alice: ")

key_a = sha256(long_to_bytes(pow(gb_attacker, a, p))).digest()[-BLOCK_SIZE:]
aes_a = AES.new(key_a, AES.MODE_ECB)

key_b = sha256(long_to_bytes(pow(ga_attacker, b, p))).digest()[-BLOCK_SIZE:]
aes_b = AES.new(key_b, AES.MODE_ECB)

message_a = FLAG[:len(FLAG)//3]
print("Intercepted from Alice:", aes_a.encrypt(pad(message_a, BLOCK_SIZE)).hex())
input_encrypted_message(aes_b, message_a, "Send to Bob (in hex): ")

message_b = FLAG[len(FLAG)//3:]
print("Intercepted from Bob:", aes_b.encrypt(pad(message_b, BLOCK_SIZE)).hex())
input_encrypted_message(aes_a, message_b, "Send to Alice (in hex): ")

print("Well done!")
