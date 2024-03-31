import pwn

REMOTE = False
DEBUG = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50300

def xor(hex1, hex2):
    int_value1 = int(hex1, 16)
    int_value2 = int(hex2, 16)

    result_int = int_value1 ^ int_value2
    result_hex = hex(result_int)[2:].zfill(2)

    if len(result_hex) % 2 != 0:
        result_hex = '0' + result_hex

    return result_hex

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge2.py'])

# Intro
conn.recvline()
conn.recvline()
conn.recvline()

# Choose token creation
conn.sendline(b'1')

# Choose username
conn.recvline()
conn.sendline(b'?????........!!!!!!!!I am a boss')

# Choose description
conn.recvline()
conn.sendline(b'........')

# Get Token
conn.recvuntil(b'(hex): ')
token = conn.recvline()
full_token = str(token, 'utf-8').rstrip("\n")
print(full_token)


# Setup Attack
initial_plaintext = ("desc=........&user=?????........!!!!!!!!I am a boss").encode().hex()
# desc=... - .....&us - er=????? - ........ - !!!!!!!! - I am a b - oss
final_plaintext =   ("user=admin&********________****---&desc=I am a boss").encode().hex()
# user=adm - in&***** - ***_____ - ___****- - --&desc= - I am a b - oss


token_parts = [full_token[i:i+16]for i in range(0, len(full_token), 16)]
initial_plaintext_parts = [initial_plaintext[i:i+16]for i in range(0, len(initial_plaintext), 16)]
initial_plaintext_parts.insert(0, token_parts[0])                                                       # Add IV
final_plaintext_parts = [final_plaintext[i:i+16]for i in range(0, len(final_plaintext), 16)]
final_plaintext_parts.insert(0, token_parts[0])                                                         # Add IV

print(token_parts)
print(initial_plaintext_parts)
print(final_plaintext_parts)


# Modify Chipertext
final_chipertext_parts = [None] * (len(token_parts))
for i in range(len(token_parts)):
    final_chipertext_parts[i] = token_parts[i]

# i is the block we'll change
i = 4
final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])
print(f"Xor of : {initial_plaintext_parts[i+1]}, {token_parts[i]}, {final_plaintext_parts[i+1]}")

i = 1
final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])
print(f"Xor of : {initial_plaintext_parts[i+1]}, {token_parts[i]}, {final_plaintext_parts[i+1]}")

i = 0
final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])
print(f"Xor of : {initial_plaintext_parts[i+1]}, {token_parts[i]}, {final_plaintext_parts[i+1]}")

final_chipertext = ""
for i in range(len(final_chipertext_parts)):
    final_chipertext = final_chipertext + final_chipertext_parts[i]
print(final_chipertext)

# Send modified Chipertext and retrieve the Flag
conn.recvline()
conn.recvline()
conn.recvline()

conn.sendline(b'2')
conn.recvline
conn.sendline(final_chipertext)

conn.interactive()