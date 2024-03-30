import os
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor_strings(str1, str2):
    print(str1, str2)
    # Converte le stringhe in byte
    bytes1 = bytearray(str1, 'utf-8')
    bytes2 = bytearray(str2, 'utf-8')

    # Esegue l'operazione XOR byte per byte
    result = bytearray()
    for byte1, byte2 in zip(bytes1, bytes2):
        result.append(byte1 ^ byte2)

    # Gestisce il caso in cui una delle stringhe sia più lunga dell'altra
    if len(bytes1) > len(bytes2):
        for byte1 in bytes1[len(bytes2):]:
            result.append(byte1)
    elif len(bytes2) > len(bytes1):
        for byte2 in bytes2[len(bytes1):]:
            result.append(byte2)

    # Converte il risultato in una stringa
    print("Res:", str(result, 'utf-8'))
    return str(result, 'utf-8')

def xor_bytearray(bytearray1, bytearray2):
    #print("XOR:", bytearray1, bytearray2)
    result = bytearray()
    for byte1, byte2 in zip(bytearray1, bytearray2):
        result.append(byte1 ^ byte2)
        #print(result)

    return result

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


# Definisco iv+token - plaintext iniziale - plaintext finale

full_token = "3061623536366162663161393061383068e5c886f0163b3a71c2cb519368346f73ad0e6889e86e25714c7ea81f18d3ea"
    #                    6631613930613830 - 68e5c886f0163b3a - 71c2cb519368346f - 73ad0e6889e86e25 - 714c7ea81f18d3ea
    # 3061623536366162 - 6631613930613830 - 68e5c886f0163b3a - 71c2cb519368346f - 73ad0e6889e86e25 - 714c7ea81f18d3ea
    

initial_plaintext = "desc=&user=?????I am a boss"
    # desc=&us - er=????? - I am a - boss
    # 3061623536366162 - desc=&us - er=????? - I am a b - oss
    # 3061623536366162 - 646573633d267573 - 65723d3f3f3f3f3f - 4920616d20612062 - 6f7373

final_plaintext = "user=admin&desc=I am a boss"
    # user=adm - in&desc= - I am a - boss
    # 3061623536366162 - user=adm - in&desc= - I am a b - oss
    # 3061623536366162 - 757365723d61646d - 696e26646573633d - 4920616d20612062 - 6f7373


# Scompongo iv+token

iv = full_token[:BLOCK_SIZE]
token = full_token[BLOCK_SIZE:]


# Divido token - plaintext iniziale - plaintext finale

token_parts = [token[i:i+16]for i in range(0, len(token), 16)]
initial_plaintext_parts = [initial_plaintext[i:i+8]for i in range(0, len(initial_plaintext), 8)]
final_plaintext_parts = [final_plaintext[i:i+8]for i in range(0, len(final_plaintext), 8)]


initial_plaintext_parts.insert(0, iv)
final_plaintext_parts.insert(0, iv)


final_ciphertext_parts = token_parts
print(final_ciphertext_parts)

#final_ciphertext_parts[0] = (hex(initial_plaintext_parts[1].encode().hex() ^ token_parts[0]) ^ final_plaintext_parts[1].encode().hex()
    

new_token = iv
for i in range(len(final_ciphertext_parts)):
    new_token = new_token + final_ciphertext_parts[i]

# new_token = "3061623536366162663161393061383068e5c886f0163b3a71c2cb519368346f73ad0e6889e86e25714c7ea81f18d3ea"
#OLD: 3061623536366162 - 6631613930613830 - 68e5c886f0163b3a - 71c2cb519368346f - 73ad0e6889e86e25 - 714c7ea81f18d3ea

new_token_parts = [None] * 6
#new_token_parts[0] = "217774243671707c"     Ottenuto con xor di 646573633d267573 - 3061623536366162 - 757365723d61646d
#new_token_parts[1] = "6a2d7a626a2d6432"     Ottenuto con xor di 65723d3f3f3f3f3f - 696e26646573633d - 6631613930613830
new_token_parts[0] = "217774243671707c"     # IV
new_token_parts[1] = "6a2d7a626a2d6432"
new_token_parts[2] = "68e5c886f0163b3a"
new_token_parts[3] = "71c2cb519368346f"
new_token_parts[4] = "73ad0e6889e86e25"
new_token_parts[5] = "714c7ea81f18d3ea"

new_token = ""
for i in range(len(new_token_parts)):
    new_token = new_token + new_token_parts[i]


print("Old", full_token)
print("New", new_token)
login(new_token)