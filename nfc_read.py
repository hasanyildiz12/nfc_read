from smbus2 import SMBus
import time

PN532_I2C_ADDR = 0x24

# PN532 komutları
PN532_COMMAND_SAMCONFIGURATION = 0x14
PN532_COMMAND_INLISTPASSIVETARGET = 0x4A

def write_command(bus, cmd, params=[]):
    frame = [0x00, 0x00, 0xFF]
    length = len(params) + 2
    frame.append(length)
    frame.append(~length & 0xFF)
    frame.append(0xD4)
    frame.append(cmd)

    for p in params:
        frame.append(p)

    checksum = 0xD4 + cmd + sum(params)
    frame.append(~checksum & 0xFF)
    frame.append(0x00)

    bus.write_i2c_block_data(PN532_I2C_ADDR, 0x00, frame)
    time.sleep(0.1)

def read_data(bus, length):
    return bus.read_i2c_block_data(PN532_I2C_ADDR, 0x00, length)

def init_pn532(bus):
    write_command(bus, PN532_COMMAND_SAMCONFIGURATION, [0x01, 0x14, 0x01])
    time.sleep(0.1)

def read_uid(bus):
    write_command(bus, PN532_COMMAND_INLISTPASSIVETARGET, [0x01, 0x00])
    time.sleep(0.2)

    data = read_data(bus, 32)

    if len(data) < 20:
        return None

    try:
        uid_length = data[19]
        uid = data[20:20+uid_length]
        return uid
    except:
        return None

def main():
    bus = SMBus(1)

    print("PN532 başlatılıyor...")
    init_pn532(bus)

    print("Kart okut...")

    while True:
        uid = read_uid(bus)
        if uid:
            print("KART ID:", [hex(i) for i in uid])
            time.sleep(1)

if __name__ == "__main__":
    main()