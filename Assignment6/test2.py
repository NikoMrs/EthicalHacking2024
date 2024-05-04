import os
from randcrack import RandCrack
rc = RandCrack()

from ctypes import CDLL
libc = CDLL("libc.so.6")

libc.srand(os.getpid())
for i in range(624):
    rand = libc.rand()
    rc.submit(rand)

areEquals = True
while(areEquals):
    myPsw = rc.predict_random()
    rand = libc.rand()
    areEquals = not (myPsw == rand)

print(f"My psw: {myPsw}")
print(f"Random psw: {rand}")
print(f"Are equals: {areEquals}")


