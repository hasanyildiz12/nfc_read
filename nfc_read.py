#!/usr/bin/env python3
import smbus2
import time

bus = smbus2.SMBus(1)
PN532_ADDR = 0x24

def pn532_write(data):
    try:
        msg = smbus2.i2c_msg.write(PN532_ADDR, data)
        bus.i2c_rdwr(msg)
    except OSError:
        # Modül uykudaysa ilk denemede hata fırlatabilir.
        # Kısa bir süre bekleyip komutu tekrar göndererek uyandırıyoruz.
        time.sleep(0.05)
        msg = smbus2.i2c_msg.write(PN532_ADDR, data)
        bus.i2c_rdwr(msg)

def pn532_read(length):
    # PN532 I2C üzerinden önce 1 byte'lık "0x01" (Ready) sinyali gönderir.
    # Bu yüzden okuyacağımız veri miktarını 1 artırıyoruz (length + 1).
    for _ in range(10):  # Hazır olana kadar en fazla 10 kez bekle/dene
        try:
            msg = smbus2.i2c_msg.read(PN532_ADDR, length + 1)
            bus.i2c_rdwr(msg)
            resp = list(msg)
            
            if resp[0] == 0x01:  # Modül cevap vermeye hazır!
                return resp[1:]  # İlk 'Ready' byte'ını atıp asıl veriyi döndür
        except OSError:
            pass  # Henüz hazır değilse hatayı yut, döngüde tekrar dene
        
        time.sleep(0.05)
        
    print("HATA: PN532 okumaya hazır değil (Zaman aşımı)")
    return None

def init_pn532():
    print("SAMConfiguration komutu gönderiliyor (Modül uyandırılıyor)...")
    # SAMConfiguration komutu
    pn532_write([0x00, 0x00, 0xFF, 0x03, 0xFD, 0xD4, 0x14, 0x01, 0x17, 0x00])
    time.sleep(0.1)
    
    # ACK paketi 6 byte'tır.
    ack = pn532_read(6)
    if ack:
        print(f"ACK Alındı: {[hex(x) for x in ack]}")
    else:
        print("ACK alınamadı, init_pn532 başarısız!")

def read_uid():
    # InListPassiveTarget komutu (Kart arama)
    pn532_write([0x00, 0x00, 0xFF, 0x04, 0xFC, 0xD4, 0x4A, 0x01, 0x00, 0xE1, 0x00])
    time.sleep(0.2) # Okuma için biraz zaman tanı
    
    resp = pn532_read(20) # Tahmini maksimum uzunluk
    if resp:
        # Yanıt geçerli mi ve kart bulundu mu? (D5 4B)
        if len(resp) >= 8 and resp[5] == 0xD5 and resp[6] == 0x4B and resp[7] > 0:
            uid_len = resp[12]
            uid = resp[13:13+uid_len]
            return bytes(uid)
    return None

print("Başlatılıyor...")
    init_pn532()

print("Kartı okutun...")
while True:
    try:
        uid = read_uid()
        if uid:
            print("Kart ID:", uid.hex())
            time.sleep(1) # Aynı kartı üst üste saniyede 10 kere okumasın diye
        time.sleep(0.2)
    except KeyboardInterrupt:
        print("\nÇıkış yapılıyor...")
        break