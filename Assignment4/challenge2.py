#!/usr/bin/env python3
import os
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


rsa = RSA.generate(1024)
known_usernames = []

def encrypt(m):
    return pow(m, rsa.e, rsa.n)

def decrypt(c):
    return pow(c, rsa.d, rsa.n)


def new_password():
    print("Choose a username")
    username = input("> ")
    username = bytes_to_long(username.strip().encode())

    print("The password is:", encrypt(username))
    known_usernames.append(username)
    known_usernames.append(-username)

def check_password():
    print("Insert the password")
    password = input("> ")
    password = int(password.strip())
    if password < 10**7:
        print("Passwords are surely at least 8 characters long...")
        return

    username = decrypt(password)
    if username in known_usernames:
        print("Password is correct!")
    else:
        print("Invalid username:", username)


print("Welcome to the Identity Delight Provider (IDP).")
print("Use it to generate private passwords that only depend on the username,")
print("to allow users to login with just their password,")
print("so that they have only one thing to remember.")

print()
print("Here's an example password:", encrypt(bytes_to_long(FLAG)))
known_usernames.append(bytes_to_long(FLAG))
known_usernames.append(-bytes_to_long(FLAG))

for i in range(5):
    print()
    print("What do you want to do?")
    print("1. Create a new password")
    print("2. Check if a password is correct")
    option = input("> ")

    if option == "1":
        new_password()
    elif option == "2":
        check_password()
    else:
        print("Bye!")
        break
