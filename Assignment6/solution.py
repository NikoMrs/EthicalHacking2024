import pwn
from randcrack import RandCrack
rc = RandCrack()

from ctypes import CDLL
libc = CDLL("libc.so.6")

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50150

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)

# Retrieve first Password
conn.recvuntil(b":")
conn.sendline(b"1")

conn.recvuntil(b": ")
firstPsw = conn.recvline(keepends=False).decode()
print(f"First Password: {firstPsw}")

for i in range(32768):              # Iterate from 0 to (Default) Max PID possibile in Linux

    print(f"Try number {i}")
    libc.srand(i)                   # Initiate srand with seed equal to selected PID

    myPsw = ""                      # Create psw in the same way as rand_pass()
    for j in range(16):
        randNum = libc.rand()
        myPsw += chr(randNum % 0x5e + ord('!'))

    print(myPsw)

    if(myPsw == firstPsw):          # Check if myPsw is equal to the received one
        break
    
guessedPsw = ""                     # Create another psw using the same seed
for i in range(16):
    randNum = libc.rand()
    guessedPsw += chr(randNum % 0x5e + ord('!'))
    
conn.recvuntil(b":")                # Send our guessed psw and retrieve the flag
conn.sendline(guessedPsw.encode())

conn.recvuntil(b":\n")
flag = (conn.recvline(keepends=False)).decode()
print(f"Flag: {flag}")

conn.close()