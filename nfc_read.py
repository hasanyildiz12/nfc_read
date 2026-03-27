#!/usr/bin/env python3
import smbus2
import time

bus = smbus2.SMBus(1)
PN532_ADDR = 0x24

def pn532_write(data):
    bus.write_i2c_block_data(PN532_ADDR, 0, data)

def pn532_read(length):
    return bus.read_i2c_block_data(PN532_ADDR, 0, length)

def init_pn532():
    # SAM configuration
    pn532_write([0x00,0x00,0xFF,0x03,0xFD,0xD4,0x14,0x01,0x17,0x00])
    time.sleep(0.1)

def read_uid():
    # InListPassiveTarget komutu
    pn532_write([0x00,0x00,0xFF,0x04,0xFC,0xD4,0x4A,0x01,0x00,0xE1,0x00])
    time.sleep(0.1)
    try:
        resp = pn532_read(20)
        # UID uzunluğu ve UID verisi
        uid_len = resp[12]
        uid = resp[13:13+uid_len]
        return bytes(uid)
    except:
        return None

init_pn532()
print("Kartı okutun...")

while True:
    uid = read_uid()
    if uid:
        print("Kart ID:", uid.hex())
        time.sleep(1)
    time.sleep(0.2)