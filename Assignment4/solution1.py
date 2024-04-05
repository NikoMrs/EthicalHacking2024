import pwn
from Crypto.Util.number import long_to_bytes, bytes_to_long
import sys
sys.set_int_max_str_digits(50000)

REMOTE = False
DEBUG = True

IP_ADDRESS = "cyberchallenge.disi.unitn.it"
PORT = 50300

if(REMOTE):
    conn = pwn.remote(IP_ADDRESS, PORT)
else:
    conn = pwn.process(['python3', 'challenge1.py'])

conn.recvuntil(b":")
flag = int((conn.recvline(keepends=False)).decode())
print("Encrypted Flag (c): ", flag)

s = flag

# rsa_n = 135225184797352238956993252284290353963628555230609411331511579550581414665636061957438738067330864251572269029201241285142988911575674611843767430873577205717882073494901661588940787272851100218353509387874111023865399990018460435399917751526038182264491743674852523720465579662692140940284835579809428254867
# rsa_e = 65537
# rsa_d = 52111742485037889239632903240795843259615221796912756039926399638822103678766259987443318562468655988795782940957116589065281107630120969783880712180036701694226345826970040315623060661606716946939672482207627604466639683281278498223391603914187707199287118698840462523582992956328913525723035521093194955201

# def encrypt(m):
#     return pow(m, rsa_e, rsa_n)

# def decrypt(c):
#     return pow(c, rsa_d, rsa_n)

# print("Decrypted Flag: ", long_to_bytes(decrypt(flag)))

e = 65537
g = 2

c_changed = (pow(g, e)) * flag
#print("C_changed: ", c_changed)

conn.recvuntil(b"> ")
conn.sendline(b"2")
# #conn.sendafter(b"> ", b"2\n")

conn.recvuntil(b"> ")
conn.sendline(str(c_changed).encode())
# #conn.sendafter(b"> ", long_to_bytes(c_changed) + b"\n")

conn.recvuntil(b": ")
m = bytes_to_long(conn.recvline(keepends=False))
# print(type(m))
# print(type(g))
print("M: ", m)

# m = 8534438674830861736080532586958588821584855748410766699483780408859618919628926946600667782043082738564212291612143835656421869484625836039248545186610049518247820637232949176630564785971230333900916493408959245915847381927639591215374426503386590013373147174366231262500220834381082531583909398493427390739
g_inverse = 1/g
flag = m * g
print("Flag: ", long_to_bytes(flag))

conn.interactive()
