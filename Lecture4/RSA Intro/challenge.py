#!/usr/bin/env python3
import os
from Crypto.Util.number import bytes_to_long, getPrime

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


def bye():
    print("Nope.")
    quit()

def input_int(prompt, expected):
    try:
        value = int(input(prompt))
    except ValueError:
        bye()
    if value != expected:
        bye()
    return value


message = "Welcome to the second lab!"
print("Here is a message for you: " + message)
m = input_int("What is its integer representation? ", bytes_to_long(message.encode()))

p = getPrime(1024)
q = getPrime(1024)

print("First prime: " + str(p))
print("Second prime: " + str(q))
n = input_int("What is n? ", p*q)
phi = input_int("What is phi(n)? ", (p-1)*(q-1))

e = 65537
d = input_int(f"If e = {e}, what is d? ", pow(e, -1, phi))
c = input_int("What is the initial message encrypted using the given parameters? ", pow(m, e, n))

print("Finally here is a ciphertext for you: " + str(pow(bytes_to_long(FLAG), e, n)))
