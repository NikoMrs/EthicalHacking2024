import os
from randcrack import RandCrack
rc = RandCrack()

from ctypes import CDLL
libc = CDLL("libc.so.6")

from Crypto.Util.number import long_to_bytes, bytes_to_long

REMOTE = True

def getPsw(len):
    libc.srand(os.getpid())

    psw = [None]*16
    for i in range(len):
        randNum = libc.rand()
        print(randNum)
        psw[i] = randNum % 0x5e + ord('!')

    #print(psw)

    fullPsw = ""
    for i in range(len):
        fullPsw = fullPsw + chr(psw[i])

    print(fullPsw)
    return(fullPsw)

def pswToRand(psw):

    for i in range(len(psw)):
        randVal = ord(psw[i]) * 0x5e        
        print(randVal)
        rc.submit(randVal)


pswToRand(getPsw(1))
exit()

for i in range(39):

    psw = getPsw(16)

    #print(psw)
    pswToRand(psw)

psw = [None]*16
for i in range(len(psw)):
    randNum = rc.predict_randrange(0,4294967294)
    psw[i] = randNum % 0x5e + ord('!')

#print(psw)

fullPsw = ""
for i in range(len(psw)):
    fullPsw = fullPsw + chr(psw[i])

randPsw = getPsw(16)
print(f"My psw: {fullPsw}")
print(f"Random psw: {randPsw}")
print(f"Are equals: {fullPsw == randPsw}")