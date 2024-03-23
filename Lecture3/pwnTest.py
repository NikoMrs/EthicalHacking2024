import pwn
from Crypto.Cipher import AES
from Crypto.Hash import MD5

conn = pwn.remote("cyberchallenge.disi.unitn.it", 10003)

conn.recvuntil(b": ")
key = conn.recvline(keepends=False).decode()
key = bytes.fromhex(key)
print(key)

conn.recvuntil(b": ")
msg = conn.recvline(keepends=False).decode()
msg = bytes.fromhex(msg)
print(msg)

cipher = AES.new(key, AES.MODE_ECB)
crypted_msg = cipher.encrypt(msg)
print()
crypted_msg = crypted_msg.hex().encode()
conn.sendlineafter(b"? ", crypted_msg)

hash = MD5.new()
hash.update(msg)
print(hash.hexdigest())
conn.sendlineafter(b"? ", hash.hexdigest())

flag = conn.recvline()
print(flag)