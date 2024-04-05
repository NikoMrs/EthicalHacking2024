import os
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor(hex1, hex2):
    int_value1 = int(hex1, 16)
    int_value2 = int(hex2, 16)

    result_int = int_value1 ^ int_value2
    result_hex = hex(result_int)[2:].zfill(2)

    if len(result_hex) % 2 != 0:
        result_hex = '0' + result_hex

    return result_hex

BLOCK_SIZE = 16

KEY = b'\xd17\xe0\x86\x92\xebg\x1eT?\x9f\xe4^\xdd\x00]'

def login(iv_enc_token):
    try:
        iv_enc_token = bytes.fromhex(iv_enc_token)
        print(iv_enc_token)
        iv, enc_token = iv_enc_token[:BLOCK_SIZE], iv_enc_token[BLOCK_SIZE:]
        cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
        padded_token = cipher.decrypt(enc_token)
        token = unpad(padded_token, BLOCK_SIZE)
        print("token inside login function", token)

        parts = token.split(b"&")
        username = None
        description = None
        for part in parts:
            pieces = part.split(b"=")
            if pieces[0] == b"user":
                username = pieces[1]
            if pieces[0] == b"desc":
                description = pieces[1]

        if username == b"admin" and description == b"I am a boss":
            print("FLAG")
        else:
            print("Welcome back", username.decode())
            print("Username: ", username.decode())
            print("Description: ", description.decode())
    except (ValueError, IndexError):
        print("Nope")

def signup(username, description):
    #print("length: ", len(f"desc={description}&user={username}"))
    print(len(f"desc={description}&user={username}"))
    token = f"desc={description}&user={username}".encode()
    #print("encoded length: ", len(token))

    padded_token = pad(token, BLOCK_SIZE)

    iv = os.urandom(BLOCK_SIZE)
    iv = b'0ab566abf1a90a80'
    cipher = AES.new(key=KEY, mode=AES.MODE_CBC, iv=iv)
    enc_token = cipher.encrypt(padded_token)
    return(iv.hex() + enc_token.hex())



full_token = signup("?????........!!!!!!!!I am a boss", "........")     # 1st parameter is the username, 2nd is the description
# With this input we only need to properly change the 5th, 2nd and 1st block.
# The last 2 blocks should be unchanged, while the 3rd and 4th will get dirty without compromising the attack

# Setup Attack
initial_plaintext = ("desc=........&user=?????........!!!!!!!!I am a boss").encode().hex()
# desc=... - .....&us - er=????? - ........ - !!!!!!!! - I am a b - oss         P  Blocks
final_plaintext =   ("user=admin&********________*******&desc=I am a boss").encode().hex()
# user=adm - in&***** - ***_____ - ___***** - **&desc= - I am a b - oss         P' Blocks

token_parts = [full_token[i:i+16]for i in range(0, len(full_token), 16)]                                # Divide in blokcs
initial_plaintext_parts = [initial_plaintext[i:i+16]for i in range(0, len(initial_plaintext), 16)]      
initial_plaintext_parts.insert(0, token_parts[0])                                                       # Add IV
final_plaintext_parts = [final_plaintext[i:i+16]for i in range(0, len(final_plaintext), 16)]
final_plaintext_parts.insert(0, token_parts[0])                                                         # Add IV

# Modify Chipertext
final_chipertext_parts = [None] * (len(token_parts))
for i in range(len(token_parts)):
    final_chipertext_parts[i] = token_parts[i]

i = 4       # i = 4 will change the plaintext block containing !!!!!!!!
final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])
i = 1       # i = 4 will change the plaintext block containing .....&us
#final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])
i = 0       # i = 4 will change the plaintext block containing desc=...
#final_chipertext_parts[i] = xor(xor(initial_plaintext_parts[i+1], token_parts[i]), final_plaintext_parts[i+1])

final_chipertext = ""
for i in range(len(final_chipertext_parts)):
    final_chipertext = final_chipertext + final_chipertext_parts[i]

print("Old", full_token)
print("New", final_chipertext)
login(final_chipertext)