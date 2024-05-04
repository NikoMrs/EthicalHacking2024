import pwn
from randcrack import RandCrack
rc = RandCrack()

from ctypes import CDLL
libc = CDLL("libc.so.6")

from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50150

allPsw = []
for i in range(1000):

    print(f"Tentativo {i}")

    if(REMOTE):
        conn = pwn.remote(IP_ADDRESS, PORT)
    else:
        conn = pwn.process(['python3', 'challenge1.py'])

    conn.recvuntil(b":")
    conn.sendline(b"1")

    conn.recvuntil(b": ")
    firstPsw = conn.recvline(keepends=False).decode()

    if firstPsw not in allPsw:
        
        allPsw.append(firstPsw)
        conn.recvuntil(b":")
        conn.sendline(b"1")

        conn.recvuntil(b": ")
        secondPsw = conn.recvline(keepends=False).decode()

        allPsw.append(secondPsw)
        conn.close()

    else:

        print("Trovato")
        index = allPsw.index(firstPsw)
        conn.recvuntil(b":")
        conn.sendline(allPsw[index+1].encode())
        break;

conn.interactive()