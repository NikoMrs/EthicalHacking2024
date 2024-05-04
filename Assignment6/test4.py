import pwn
from randcrack import RandCrack
rc = RandCrack()

from ctypes import CDLL
libc = CDLL("libc.so.6")

from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50150

def pswToRand(psw):

    for i in range(len(psw)):
        randVal = (ord(psw[i]) - ord('!')) % 0x5e
        rc.submit(randVal)


for i in range(39):
    if(REMOTE):
        conn = pwn.remote(IP_ADDRESS, PORT)
    else:
        conn = pwn.process(['python3', 'challenge1.py'])

    conn.recvuntil(b":")
    conn.sendline(b"1")

    conn.recvuntil(b": ")
    psw = conn.recvline(keepends=False).decode()

    print(psw)
    pswToRand(psw)

    conn.close()

# currentTime = libc.time(0)

# libc.srand(currentTime)

# psw = [None]*16
# for i in range(len(psw)):
#     randNum = libc.rand()
#     psw[i] = randNum % 0x5e + ord('!')

# print(psw)

# fullPsw = ""
# for i in range(len(psw)):
#     fullPsw = fullPsw + chr(psw[i])

# print(fullPsw)

# conn.recvuntil(b":")
# conn.sendline(fullPsw.encode())

psw = [None]*16
for i in range(len(psw)):
    randNum = rc.predict_randrange(0,4294967294)
    psw[i] = randNum % 0x5e + ord('!')

print(psw)

fullPsw = ""
for i in range(len(psw)):
    fullPsw = fullPsw + chr(psw[i])

print(fullPsw)

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge1.py'])

# conn.recvuntil(b":")
# conn.sendline(myRand.encode())


conn.interactive()