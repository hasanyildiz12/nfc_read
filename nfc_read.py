#!/usr/bin/env python3
import smbus2
import time

bus = smbus2.SMBus(1)
PN532_ADDR = 0x24

def pn532_write(data):
    msg = smbus2.i2c_msg.write(PN532_ADDR, data)
    bus.i2c_rdwr(msg)

def pn532_read(length):
    msg = smbus2.i2c_msg.read(PN532_ADDR, length)
    bus.i2c_rdwr(msg)
    return list(msg)

def init_pn532():
    pn532_write([0x00,0x00,0xFF,0x03,0xFD,0xD4,0x14,0x01,0x17,0x00])
    time.sleep(0.1)
    pn532_read(6)  # ACK oku

def read_uid():
    pn532_write([0x00,0x00,0xFF,0x04,0xFC,0xD4,0x4A,0x01,0x00,0xE1,0x00])
    time.sleep(0.5)
    try:
        resp = pn532_read(20)
        if resp[5] == 0xD5 and resp[6] == 0x4B and resp[7] > 0:
            uid_len = resp[12]
            uid = resp[13:13+uid_len]
            return bytes(uid)
    except:
        pass
    return None

print("Başlatılıyor...")
init_pn532()
print("Kartı okutun...")

while True:
    uid = read_uid()
    if uid:
        print("Kart ID:", uid.hex())
        time.sleep(1)
    time.sleep(0.2)