import pwn

REMOTE = False
DEBUG = True

IP_ADDRESS = 1
PORT = 2

def debug(msg):
    if(DEBUG):
        print(msg)

def createToken(username, description):

    print(f"Creo un nuovo TOKEN username: {username} - description: {description}")

    conn.sendline(b'1')                 # Send option

    username = bytes(username)
    description = bytes(description)

    line = conn.recvuntil(b'> ')        # Username msg

    debug(line)
    conn.sendline(username)             # Send username

    line = conn.recvuntil(b'> ')        # Description msg
    debug(line)
    conn.sendline(description)          # Send description

    line = conn.recvuntil(b'(hex): ')   # Token msg
    debug(line)
    token = conn.recvline()             # Token
    debug(token)


    line = conn.recvuntil(b'> ')        # Option select msg
    debug(line)

    return token


def useToken(token):

    print(f"Uso il TOKEN {token}")

    conn.sendline(b'2')                 # Send option

    token = bytes(token)

    line = conn.recvuntil(b'> ')        # Login msg
    debug(line)
    conn.sendline(token)                # Send token

    line = conn.recvline()              # Result msg
    debug(line)


    line = conn.recvuntil(b'> ')        # Option select msg
    debug(line)


if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge.py'])


#line = conn.recvuntil(b'> ')            # Intro msg
#debug(line)

username = b'Nicola'
description = b'Test'

#token = createToken(username, description)
#useToken(token)

username = b'Nicola1'
description = b'Test1'

#token = createToken(username, description)
#useToken(token)

conn.interactive()