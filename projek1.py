import pandas as pd
import warnet
from warnet import harga_perjam

menu = [
    {"no": 1, "item": "Indomie", "harga": 8000},
    {"no": 2, "item": "Kentang Goreng", "harga": 10000},
    {"no": 3, "item": "Mix Platter", "harga": 18000},
    {"no": 4, "item": "Cireng Isi Ayam", "harga": 13000},
    {"no": 5, "item": "Risol Mayo", "harga": 13000},
    {"no": 6, "item": "Roti Bakar", "harga": 10000},
    {"no": 7, "item": "Pisang Coklat Keju", "harga": 10000},
    {"no": 8, "item": "Kopi", "harga": 5000},
    {"no": 9, "item": "Ice Non Coffe", "harga": 5000},
    {"no": 10, "item": "Susu Ovaltine", "harga": 7000},
]

def input_orders():
    orders = []
    while True:
        print("\n============ DAFTAR MENU ============")
        for m in menu:
            print(f"{m['no']}. {m['item']} - Rp{m['harga']}")
        print("====================================")

        pilihan = int(input('Pilih nomor menu, "0" untuk selesai: '))
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

def cetak_detail_warnet(nama, jam_main):
    harga = warnet.harga_perjam
    total = warnet.hitung_biaya(jam_main)

    print("Detail Order Warnet :")
    print(f"Nama         : {nama}") 
    print(f"Jam Main     : {jam_main} Jam")
    print(f"Harga/Jam    : Rp {harga}")
    print(f"Total Warnet : Rp {total}")
    print("----------------------------------------------")
    return total

def cetak_rincian(nama, jam_main, orders):
    subtotal_makanan = sum(o["jumlah"] * o["harga"] for o in orders)
    totalwarnet = warnet.hitung_biaya(jam_main)
    total = totalwarnet + subtotal_makanan

    order_menu = pd.DataFrame(orders) if orders else pd.DataFrame(columns=["item", "jumlah", "harga"])
    if not order_menu.empty:
        order_menu["subtotal"] = order_menu["jumlah"] * order_menu["harga"]

    print("----------------------------------------------")
    print("------------- RINCIAN PEMBAYARAN -------------")
    print("----------------------------------------------")

    biaya_warnet = cetak_detail_warnet(nama, jam_main)

    print("-----------   Makanan & Minuman   ------------")
    print("----------------------------------------------")
    if order_menu.empty:
        print("Tidak ada pemesanan makanan/minuman")
    else:
        print(order_menu.to_string(index=False))
    print("----------------------------------------------")
    print(f"\t\tOrder Warnet       : {biaya_warnet}")
    print(f"\t\tMakanan & Minuman  : {subtotal_makanan}")
    print(f"\t\tTotal              : {total}")
    print("----------------------------------------------")
    return total

def cetak_struk(nama, jam_main, orders, total, tunai):
    kembali = tunai - total

    order_menu = pd.DataFrame(orders) if orders else pd.DataFrame(columns=["item", "jumlah", "harga"])
    if not order_menu.empty:
        order_menu["subtotal"] = order_menu["jumlah"] + order_menu["harga"]
    print("\n----------------------------------------------")
    print("--------------- STRUK CALF NET ---------------")
    print("----------------------------------------------")

    biaya_warnet = cetak_detail_warnet(nama, jam_main)

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
jam_main = int(input("Jam Main : "))
orders = input_orders()

total = cetak_rincian(nama, jam_main, orders)

while True:
    tunai = int(input("Masukkan uang tunai : "))
    if tunai < total:
        print("Uang tidak cukup, silahkan masukkan lagi!")
    else:
        break

cetak_struk(nama, jam_main, orders, total, tunai)