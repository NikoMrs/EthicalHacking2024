#!/usr/bin/env python3
import os
import hashlib

if os.path.exists("./flag.txt"):
    with open("./flag.txt", "r") as f:
        FLAG = f.read().strip()
else:
    FLAG = "UniTN{placeholder_flag}"


salt = os.urandom(32)
users = {
    "richperson": 100,
}
goods = {
    "pizza": (5, "Margherita"),
    "game": (10, "Card deck"),
    "flag": (20, FLAG),
}
current_user = None

def generate_password(token: bytes) -> str:
    return hashlib.sha1(salt + token).hexdigest()

def signup():
    print("Which username do you want?")
    username = input("> ")
    if username in users:
        print("Username already taken")
        return
    print("Insert your real name")
    real_name = input("> ")
    if "|" in username or "|" in real_name:
        print("No hacks please")
        return

    # welcome bonus money to encourage creating accounts
    users[username] = 10
    token = (real_name + "||||" + username).encode()
    print(f"Your login token is: {token.hex()}")
    print(f"And your password is: {generate_password(token)}")

def login():
    print("Insert your login token")
    token = bytes.fromhex(input("> "))
    print("Insert your password")
    password = input("> ")

    if generate_password(token) != password:
        print("Wrong login token or password")
        return

    print("Welcome back", token.split(b"||||")[0].decode())
    global current_user
    current_user = token.split(b"||||")[-1].decode()

def buy():
    print("Select the good to buy:")
    for (good, (price, _)) in goods.items():
        print(f"- {good}: {price}€")
    good = input("> ")
    price, content = goods[good]
    if price <= users[current_user]:
        users[current_user] -= price
        print(f"Here it is: {content}")
    else:
        print("You don't have enough money...")

while True:
    print("Welcome to myHL&E, where you can manage your accounts")
    if current_user is not None:
        print(f"You are logged in as {current_user} and you own {users[current_user]}€")
    print("What do you want to do?")
    print("1. Create a new bank account")
    print("2. Login to your bank account")
    if current_user is not None:
        print("3. Buy something")
    option = input("> ")

    if option == "1":
        signup()
    elif option == "2":
        login()
    elif option == "3" and current_user is not None:
        buy()
    else:
        print("Bye!")
        break
    print()

