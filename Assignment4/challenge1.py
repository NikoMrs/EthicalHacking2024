#!/usr/bin/env python3
import os
from Crypto.PublicKey import RSA
from Crypto.Util.number import bytes_to_long, long_to_bytes

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "rb") as f:
        FLAG = f.read().strip()
else:
    FLAG = b"UniTN{placeholder_flag}"


rsa = RSA.generate(1024)
known_usernames = []

#print(rsa.n, rsa.e, rsa.d)
rsa_n = 135225184797352238956993252284290353963628555230609411331511579550581414665636061957438738067330864251572269029201241285142988911575674611843767430873577205717882073494901661588940787272851100218353509387874111023865399990018460435399917751526038182264491743674852523720465579662692140940284835579809428254867
rsa_e = 65537
rsa_d = 52111742485037889239632903240795843259615221796912756039926399638822103678766259987443318562468655988795782940957116589065281107630120969783880712180036701694226345826970040315623060661606716946939672482207627604466639683281278498223391603914187707199287118698840462523582992956328913525723035521093194955201

def encrypt(m):
    print(pow(m, rsa_e, rsa_n))
    return pow(m, rsa_e, rsa_n)

def decrypt(c):
    return pow(c, rsa_d, rsa_n)


def new_password():
    print("Choose a username")
    username = input("> ")
    username = bytes_to_long(username.strip().encode())

    print("The password is:", encrypt(username))
    known_usernames.append(username)

def check_password():
    print("Insert the password")
    password = input("> ")
    password = int(password.strip())

    username = decrypt(password)
    if username in known_usernames:
        print("Password is correct!")
    else:
        print("Invalid username:", username)


print("Welcome to the Identity Delight Provider (IDP).")
print("Use it to generate private passwords that only depend on the username,")
print("to allow users to login with just their password,")
print("so that they have only one thing to remember.")

#print(bytes_to_long(FLAG))
res = encrypt(bytes_to_long(FLAG))
print("Here's an example password:", res)
#print("Decrypted: ", long_to_bytes(decrypt(res)))
known_usernames.append(bytes_to_long(FLAG))

while True:
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
