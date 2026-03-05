import pandas as pd
import room
from room import harga_perjam

print("----------------------------------------------")
print("-------- Selamat Datang di RamCoffee ---------")
print("----------------------------------------------")

menu = [
    {"no": 1, "item": "Americano", "harga": 23000},
    {"no": 2, "item": "Cappucino", "harga": 25000},
    {"no": 3, "item": "Caffe Latte", "harga": 25000},
    {"no": 4, "item": "Matcha Latte", "harga": 25000},
    {"no": 5, "item": "Chocolate", "harga": 25000}, 
]


def input_orders():
    orders = []
    while True:
        print("\n============ DAFTAR MENU ============")
        for m in menu:
            print(f"{m['no']}. {m['item']} - Rp{m['harga']}")
        print("====================================")

        pilihan = int(input('Pilih nomor menu, ketik "0" untuk selesai: '))
        if pilihan == 0:
            break
        if pilihan not in (m["no"] for m in menu):
            print("Menu tidak tersedia, silhkan coba kembali!")
            continue
        jumlah = int(input("Masukkan jumlah: "))
        for m in menu:
            if m["no"] == pilihan:
                orders.append({"item": m["item"], "jumlah": jumlah, "harga": m["harga"]})
    return orders

def cetak_detail_room(nama, jam_main):
    harga = room.harga_perjam
    total = room.hitung_biaya(jam_main)

    print("Detail Order Sewa Private Room :")
    print(f"Nama         : {nama}") 
    print(f"Jam Main     : {jam_main} Jam")
    print(f"Harga/Jam    : Rp {harga}")
    print(f"Total Sewa   : Rp {total}")
    print("----------------------------------------------")
    return total

def cetak_rincian(nama, jam_main, orders):
    subtotal_makanan = sum(o["jumlah"] * o["harga"] for o in orders)
    totalroom = room.hitung_biaya(jam_main)
    total = totalroom + subtotal_makanan

    order_menu = pd.DataFrame(orders) if orders else pd.DataFrame(columns=["item", "jumlah", "harga"])
    if not order_menu.empty:
        order_menu["subtotal"] = order_menu["jumlah"] * order_menu["harga"]

    print("----------------------------------------------")
    print("------------- RINCIAN PEMBAYARAN -------------")
    print("----------------------------------------------")

    biaya_room = cetak_detail_room(nama, jam_main)

    print("-----------   Makanan & Minuman   ------------")
    print("----------------------------------------------")
    if order_menu.empty:
        print("Tidak ada pemesanan makanan/minuman")
    else:
        print(order_menu.to_string(index=False))
    print("----------------------------------------------")
    print(f"\t\tOrder Warnet       : {biaya_room}")
    print(f"\t\tMakanan & Minuman  : {subtotal_makanan}")
    print(f"\t\tTotal              : {total}")
    print("----------------------------------------------")
    return total

from datetime import datetime

def cetak_struk(nama, jam_main, orders, total, tunai):
    tanggal = datetime.now().strftime("%d-%m-%Y %H:%M")
    kembali = tunai - total

    order_menu = pd.DataFrame(orders) if orders else pd.DataFrame(columns=["item", "jumlah", "harga"])
    if not order_menu.empty:
        order_menu["subtotal"] = order_menu["jumlah"] + order_menu["harga"]
    print("\n----------------------------------------------")
    print("--------------- STRUK RAMCOFFEE --------------")
    print("----------------------------------------------")
    print(f"Tanggal      : {tanggal}")
    
    biaya_room = cetak_detail_room(nama, jam_main)

    print("-----------   Makanan & Minuman   ------------")
    print("----------------------------------------------")

    if order_menu.empty:
        print("Tidak ada pemesanan makanan/minuman")
    else:
        print(order_menu.to_string(index=False))
    print("----------------------------------------------")

    print(f"\t\t\tTotal     : {total}")
    print(f"\t\t\tTunai     : {tunai}")
    print(f"\t\t\tKembali   : {kembali}")
    print("----------------------------------------------")

nama = input("Masukkan nama pelanggan: ")
jam_sewa = int(input("Jam Sewa Private Room: "))
orders = input_orders()

total = cetak_rincian(nama, jam_sewa, orders)

while True:
    tunai = int(input("Masukkan uang tunai : "))
    if tunai < total:
        print("Uang tidak cukup, silahkan masukkan lagi!")
    else:
        break

cetak_struk(nama, jam_sewa, orders, total, tunai)