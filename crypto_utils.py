import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from RC6Encryption import RC6Encryption

def aes_encrypt(data: bytes, key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv + ct_bytes

def aes_decrypt(data: bytes, key: bytes) -> bytes:
    iv = data[:AES.block_size]
    ct = data[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

import struct

def rc6_encrypt(data: bytes, key: bytes) -> bytes:
    rc6 = RC6Encryption(key)
    padded_data = pad(data, 16)
    iv = os.urandom(16)
    ct = bytearray()
    prev = iv
    
    for i in range(0, len(padded_data), 16):
        block = bytearray(padded_data[i:i+16])
        # CBC XOR
        for j in range(16):
            block[j] ^= prev[j]
        # encrypt block (RC6 returns list of 4 ints)
        enc_ints = rc6.encrypt(bytes(block))
        # pack to bytes
        enc_block = struct.pack('<4I', *enc_ints)
        ct.extend(enc_block)
        prev = enc_block
    return iv + bytes(ct)

def rc6_decrypt(data: bytes, key: bytes) -> bytes:
    rc6 = RC6Encryption(key)
    iv = data[:16]
    ct = data[16:]
    pt = bytearray()
    prev = iv
    
    for i in range(0, len(ct), 16):
        enc_block = ct[i:i+16]
        # unpack to 4 ints
        enc_ints = list(struct.unpack('<4I', enc_block))
        # decrypt block (RC6 returns list of 4 ints)
        dec_ints = rc6.decrypt(enc_ints)
        dec_block = bytearray(struct.pack('<4I', *dec_ints))
        # CBC XOR
        for j in range(16):
            dec_block[j] ^= prev[j]
        pt.extend(dec_block)
        prev = enc_block
    return unpad(bytes(pt), 16)
