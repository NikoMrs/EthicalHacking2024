import os
import string
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def xor_strings(str1, str2):
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

full_token = "0ab566abf1a90a805b0b11657e3a33a8c2188773fe19b7594d6032c82d92edeaa7577a494452880b9f0e0be8e617aa6e"
    # 0ab566abf1a90a80 - 5b0b11657e3a33a8 - c2188773fe19b759 - 4d6032c82d92edea - a7577a494452880b - 9f0e0be8e617aa6e

initial_plaintext = "desc=I am a boss&user=?dmin"
    # desc=I_a - m_a_boss - &user=?d - min_-_-_

final_plaintext = "desc=I am a boss&user=admin"
    # desc=I_a - m_a_boss - &user=ad - min_-_-_


# Scompongo iv+token

iv = full_token[:BLOCK_SIZE]
    # 0ab566abf1a90a80
token = full_token[BLOCK_SIZE:]
    # 5b0b11657e3a33a8 - c2188773fe19b759 - 4d6032c82d92edea - a7577a494452880b - 9f0e0be8e617aa6e


# Divido token - plaintext iniziale - plaintext finale

token_parts = [token[i:i+16]for i in range(0, len(token), 16)]
initial_plaintext_parts = [initial_plaintext[i:i+8]for i in range(0, len(initial_plaintext), 8)]
final_plaintext_parts = [final_plaintext[i:i+8]for i in range(0, len(final_plaintext), 8)]


# Creo degli array di bytearray con le varie parti di token - plaintext iniziale - plaintext finale

token_parts_bytes = [None] * len(token_parts)
initial_plaintext_parts_bytes = [None] * (len(initial_plaintext_parts) + 1)
final_plaintext_parts_bytes = [None] * (len(final_plaintext_parts) + 1)

for i in range(len(token_parts)):
    token_parts_bytes[i] = bytearray(token_parts[i], 'utf-8')

#print(initial_plaintext_parts, len(initial_plaintext_parts))
for i in range(len(initial_plaintext_parts)):
    initial_plaintext_parts_bytes[i+1] = bytearray(initial_plaintext_parts[i], 'utf-8')
    final_plaintext_parts_bytes[i+1] = bytearray(final_plaintext_parts[i], 'utf-8')


# Aggiungo agli array di bytearry l'iv  --> Dimensione di 5 Blocchi

initial_plaintext_parts_bytes[0] = bytearray(iv.encode())
final_plaintext_parts_bytes[0] = bytearray(iv.encode())


new_token = bytearray(iv.encode())

# print("Token", token_parts_bytes)
# print("Plaintext iniziale", initial_plaintext_parts_bytes)
# print("Plaintext desiderato", final_plaintext_parts_bytes)

final_ciphertext_parts_bytes = token_parts_bytes
for i in range(2,-1,-1):

    # final_plaintext = final_plaintext_parts[i]              # Pi'
    # initial_plaintext = initial_plaintext_parts[i]          # Pi
    # if(i == 0):                                             # Ci-1
    #     initial_ciphertext = iv
    # else:
    #     initial_ciphertext = token_parts[i-1]                 

    # print(f"Block #{i}:", f"FinalPlain: {final_plaintext_parts_bytes[i]}, \
    #       InitialPlain: {initial_plaintext_parts_bytes[i]}, InitialChiper: {token_parts_bytes[i-1]}")

    #final_ciphertext[i] = xor_strings(xor_strings(initial_plaintext, initial_ciphertext), final_plaintext)
    if(i == 0):
        print("New Token", new_token)
        print("Plaintext", initial_plaintext_parts_bytes[i])
        aux = xor_bytearray(initial_plaintext_parts_bytes[i], new_token)
    else:
        aux = xor_bytearray(initial_plaintext_parts_bytes[i], token_parts_bytes[i-1])

    print(f"aux {i}:", aux.hex())
    aux = bytearray(aux.hex(), 'utf-8')
    print(f"aux hex {i}:", aux)
    final_ciphertext_parts_bytes[i-1] = bytearray(xor_bytearray(aux, final_plaintext_parts_bytes[i]).hex(), 'utf-8')
    print(f"Block #{i}:", final_ciphertext_parts_bytes[i])


#desired_plaintext = "&user=ad"                     # Pi'
#current_plaintext = "&user=?d"                     # Pi
#previous_ciphertext = "a3667c3a183b27c7"                    # Ci-1

#iv = xor_strings(desired_plaintext, xor_strings(current_plaintext, previous_ciphertext)) 
#print(iv)

#new_token = iv + token
#print(new_token)

for i in range(len(final_ciphertext_parts_bytes)):
    new_token = new_token + final_ciphertext_parts_bytes[i]
new_token = str(new_token, 'utf-8')

print("Old", full_token)
print("New", new_token)
login(new_token)