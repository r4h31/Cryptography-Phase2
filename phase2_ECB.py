from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def jadikan_16(teks):
    while len(teks) < 16:
        teks = teks + " "
    return teks

nama = ["andi", "budi", "citra", "dewi", "eka", "fajar", "gita", "hadi", "indra", "joko"]
status = ["LULUS", "TIDAK LULUS", "LULUS", "LULUS", "MENGULANG",
          "LULUS", "TIDAK LULUS", "LULUS", "MENGULANG", "LULUS"]

pesan = ""
for s in status:
    pesan = pesan + jadikan_16(s)
pesan = pesan.encode()

kunci = b"kuncirahasia1234"

def pecah_blok(data):
    daftar = []
    for i in range(0, len(data), 16):
        daftar.append(data[i:i + 16])
    return daftar

# Experiment 1
ecb = AES.new(kunci, AES.MODE_ECB)
hasil_ecb = ecb.encrypt(pesan)
blok_ecb = pecah_blok(hasil_ecb)

print("Percobaan 1")
for i in range(len(nama)):
    print(nama[i], blok_ecb[i].hex())

unik = []
for b in blok_ecb:
    if b not in unik:
        unik.append(b)
print("Jumlah blok:", len(blok_ecb))
print("Jumlah blok berbeda:", len(unik))


# Experiment 2
print("\nPercobaan 2")
frekuensi = {}
for b in blok_ecb:
    if b in frekuensi:
        frekuensi[b] = frekuensi[b] + 1
    else:
        frekuensi[b] = 1

for b in frekuensi:
    print(b.hex(), "muncul", frekuensi[b], "kali")

blok_andi = blok_ecb[0]
for i in range(len(nama)):
    if blok_ecb[i] == blok_andi:
        print(nama[i], "-> sama dengan andi, berarti LULUS")
    else:
        print(nama[i], "-> beda dengan andi, belum diketahui")


# Experiment 3
print("\nPercobaan 3")
ecb2 = AES.new(kunci, AES.MODE_ECB)
hasil_ecb2 = ecb2.encrypt(pesan)
print("ECB dijalankan dua kali, apakah hasil sama?", hasil_ecb == hasil_ecb2)

iv1 = get_random_bytes(16)
iv2 = get_random_bytes(16)
cbc1 = AES.new(kunci, AES.MODE_CBC, iv1)
cbc2 = AES.new(kunci, AES.MODE_CBC, iv2)
hasil_cbc1 = cbc1.encrypt(pesan)
hasil_cbc2 = cbc2.encrypt(pesan)
print("CBC dijalankan dua kali, apakah hasil sama?", hasil_cbc1 == hasil_cbc2)

blok_cbc = pecah_blok(hasil_cbc1)
unik_cbc = []
for b in blok_cbc:
    if b not in unik_cbc:
        unik_cbc.append(b)
print("Jumlah blok CBC:", len(blok_cbc))
print("Jumlah blok CBC berbeda:", len(unik_cbc))
for i in range(len(nama)):
    print(nama[i], blok_cbc[i].hex())