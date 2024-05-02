import pwn

from ctypes import CDLL
libc = CDLL("libc.so.6")

from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50150

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge1.py'])

currentTime = libc.time(0)

libc.srand(currentTime)

psw = [None]*16
for i in range(len(psw)):
    randNum = libc.rand()
    psw[i] = randNum % 0x5e + ord('!')

print(psw)

fullPsw = ""
for i in range(len(psw)):
    fullPsw = fullPsw + chr(psw[i])

print(fullPsw)

conn.recvuntil(b":")
conn.sendline(fullPsw.encode())

conn.interactive()