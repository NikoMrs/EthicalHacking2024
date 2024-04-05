#!/usr/bin/env python3
import json

MOD = 256 # allows generating bytes from 0 to 255

class LCG:
    def __init__(self, a: int, c: int, x0: int):
        self.a = a
        self.c = c
        self.x = x0

    def generate_byte(self) -> int:
        prev_x = self.x
        self.x = (self.a * self.x + self.c) % MOD
        return prev_x

with open("./data.json", "r") as f:
    data = json.load(f)
lcg = LCG(data["a"], data["c"], data["x0"])
flag = data["flag"].encode()
assert flag.startswith(b"UniTN{")

enc_flag = bytes([c ^ lcg.generate_byte() for c in flag])
with open("message.txt", "w") as f:
    f.write(enc_flag.hex())
