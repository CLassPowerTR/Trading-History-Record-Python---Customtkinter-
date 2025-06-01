import customtkinter
import tkinter as tk
from datetime import datetime
import sqlite3
from datetime import datetime, timezone, timedelta
from collections import Counter



def toplamTutarlar():
    if  donemler.get() == "Toplam":
        if gunler.get() != "Toplam":
            gunler.set("Toplam")
        try:
            conn = sqlite3.connect("gelir_gider.sqlite")
            cursor = conn.cursor()

            # Gelir tablosundaki tutarları topla
            cursor.execute("SELECT SUM(toplam_gelir) FROM gelir_kaydi")
            gelir_toplam = cursor.fetchone()[0]

            # Gider tablosundaki tutarları topla
            cursor.execute("SELECT SUM(toplam_gider) FROM gider_kaydi")
            gider_toplam = cursor.fetchone()[0]
            # Bağlantıyı kapat
            conn.close()
            
            if gelir_toplam == None or gider_toplam == None:
                pass
            else:
                kar_toplam = gelir_toplam - gider_toplam
                label3.configure(text=f"{kar_toplam:.2f}  Won")

            # Toplam gelir ve gideri yazdır
            
            label4.configure(text=f"{gelir_toplam:.2f}  Won")
            label5.configure(text=f"{gider_toplam:.2f}  Won")
            
        except sqlite3.Error as e:
            print(f"Hata: {e}")
    else:
        try:
            conn = sqlite3.connect("gelir_gider.sqlite")
            cursor = conn.cursor()
            
            if donemler.get() in donem:
                indeks = donem.index(donemler.get())
                hedef_ay = indeks
                hedef_ay = str(hedef_ay)
                if len(hedef_ay) == 1:
                    hedef_ay = f"0{hedef_ay}"
            if yillar.get() in yil:
                hedef_yil = str(yillar.get())
                
                
            if gunler.get() != "Toplam":
                hedef_gun = str(gunler.get())
                if len(hedef_gun) == 1:
                    hedef_gun = f"0{hedef_gun}"
                gelir_sorgu = "SELECT SUM(toplam_gelir) FROM gelir_kaydi WHERE strftime('%Y', gelir_tarih) = ? AND strftime('%m', gelir_tarih) = ? AND strftime('%d', gelir_tarih) = ?"
                gider_sorgu = "SELECT SUM(toplam_gider) FROM gider_kaydi WHERE strftime('%Y', gider_tarih) = ? AND strftime('%m', gider_tarih) = ? AND strftime('%d', gider_tarih) = ?"
                parametreler = (hedef_yil, hedef_ay, hedef_gun)
                # Yıl, Ay ve Güne göre verileri çek
                # Sorguyu yürüt
                cursor = conn.cursor()
                cursor.execute(gelir_sorgu, parametreler)
                gelir_veriler = cursor.fetchall()[0][0]
                cursor.execute(gider_sorgu, parametreler)
                gider_veriler = cursor.fetchall()[0][0]
            else:
                # Ay'a göre gelir ve giderleri çek
                cursor.execute("SELECT SUM(toplam_gider) FROM gider_kaydi WHERE strftime('%m', gider_tarih) = ?", (f"{hedef_ay}",))
                gider_veriler = cursor.fetchall()[0][0]
                cursor.execute("SELECT SUM(toplam_gelir) FROM gelir_kaydi WHERE strftime('%m', gelir_tarih) = ?", (f"{hedef_ay}",))
                gelir_veriler = cursor.fetchall()[0][0]
                
            conn.close()
            
            
            if gelir_veriler == None and gider_veriler == None:
                label3.configure(text=f"{donemler.get()} ait veri Yoktur...")
                label4.configure(text=f"{donemler.get()} ait veri Yoktur...")
                label5.configure(text=f"{donemler.get()} ait veri Yoktur...")
            # Toplam gelir ve gideri yazdır
            else:
                if gelir_veriler == None:
                    gelir_veriler = 0
                if gider_veriler == None:
                    gider_veriler = 0
                kar_toplam = gelir_veriler - gider_veriler
                label3.configure(text=f"{kar_toplam:.2f}  Won")
                label4.configure(text=f"{gelir_veriler:.2f}  Won")
                label5.configure(text=f"{gider_veriler:.2f}  Won")
            

        except sqlite3.Error as e:
            print(f"Hata: {e}")

def donemSec():
    toplamTutarlar()

def kayitli_yillar():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    
    # Gelir tablosundaki tutarları topla
    cursor.execute("SELECT DISTINCT strftime('%Y', gelir_tarih) AS yıl FROM gelir_kaydi")
    kayitliGelir_yillar = cursor.fetchone()

    # Bağlantıyı kapat
    conn.close()
    
    return kayitliGelir_yillar

def kayitli_gunler():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    

    cursor.execute("SELECT DISTINCT strftime('%d', gelir_tarih) AS gün FROM gelir_kaydi")
    kayitliGelir_gunler = cursor.fetchall()
    
    cursor.execute("SELECT DISTINCT strftime('%d', gider_tarih) AS gün FROM gider_kaydi")
    kayitliGider_gunler = cursor.fetchall()
    
    gelir_liste = [str(i[0]) for i in kayitliGelir_gunler]
    gider_liste = [str(i[0]) for i in kayitliGider_gunler]
     
        
    for i in gider_liste:
        if i not in  gelir_liste:
            gelir_liste.append(i)
     
    # Bağlantıyı kapat
    conn.close()
    gelir_liste.sort(reverse=False)
    return gelir_liste

def yilSec_OptionMenuUpdate():
    yil = kayitli_yillar()
    yillar.configure(values=yil)

def yilSec_OptionMenu():
    global yillar, yil
    
    yil = kayitli_yillar()
    yillar = customtkinter.CTkOptionMenu(gelir_gider, values=yil, corner_radius=15,font=("Bold", 12, "bold"),fg_color='#404040')
    yillar.grid(row=0, column=0, padx=(50,0), pady=(10,0))

def donemSec_OptionMenu(gelir_gider):
    global donemler, donem
    donem = ["Toplam","Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]
    donemler = customtkinter.CTkOptionMenu(gelir_gider, values=donem, corner_radius=15,font=("Bold", 12, "bold"),fg_color='#404040')
    donemler.grid(row=0, column=0,columnspan=2, padx=(100,0), pady=(10,0))
    donemler.set("Toplam")
    #toplamTutarlar()

def gunSec_OptionMenuUpdate():
    gun = kayitli_gunler()
    gun.insert(0,"Toplam")
    gunler.configure(values=gun)

def gunSec_OptionMenu():
    global gunler, gun
    gun = kayitli_gunler()
    gun.insert(0,"Toplam")
    gunler = customtkinter.CTkOptionMenu(gelir_gider, values=gun, corner_radius=15,font=("Bold", 12, "bold"),fg_color='#404040')
    gunler.grid(row=0, column=1, padx=(200,0), pady=(10,0))
    gunler.set("Toplam")
    #toplamTutarlar()

def rapor_olusturma_button(gelir_gider):
    rapor_olustur_butonu = customtkinter.CTkButton(gelir_gider, text="Rapor Oluştur",width=90, command=donemSec,corner_radius=15, font = ("Bold", 12, "bold"))
    rapor_olustur_butonu.grid(row=0, column=2, padx=(0,0), pady=(10,0))
    
def boyut_degisti(event):
    label_width = int(event.width * 0.15)
    label_height = int(event.height * 0.035)
    combobox_width = int(event.width * 0.1)
    combobox_height = int(event.height * 0.035)
    
    label.configure(width=label_width, height=label_height)
    label1.configure(width=label_width, height=label_height)
    label2.configure(width=label_width, height=label_height)
    label3.configure(width=label_width, height=label_height * 2)
    label4.configure(width=label_width, height=label_height * 2)
    label5.configure(width=label_width, height=label_height * 2)
    
    gunler.configure(width=combobox_width)
    donemler.configure(width=combobox_width)
    yillar.configure(width=combobox_width)
    
def labels(gelir_gider):
    global label3, label4, label5, label, label1, label2
    #Label boyuWonarı
    label_corner_radius=3
    label_font = ("Ariel", 15, "bold")
    label_color = "#1ab394"

    
    label = customtkinter.CTkLabel(gelir_gider, text="Kar", fg_color=label_color,font=label_font, corner_radius=label_corner_radius)
    label.grid(row=1, column=0, padx=(40,0), pady=(30,0))#.place(relx=0.05, rely=0.12)
    label1 = customtkinter.CTkLabel(gelir_gider, text="Toplam Gelir", fg_color=label_color,font=label_font, corner_radius=label_corner_radius)
    label1.grid(row=1, column=1, padx=(40,0), pady=(30,0))
    label2 = customtkinter.CTkLabel(gelir_gider, text="Toplam Gider", fg_color=label_color,font=label_font, corner_radius=label_corner_radius)
    label2.grid(row=1, column=2, padx=(40,0), pady=(30,0))
    
    label3 = customtkinter.CTkLabel(gelir_gider, text="  Won", fg_color="#23c5c7",font=("Ariel", 22, "bold"), corner_radius=label_corner_radius,anchor="e")
    label3.grid(row=2, column=0, padx=(40,0), pady=(10,0))
    label4 = customtkinter.CTkLabel(gelir_gider, text="  Won", fg_color="#309dd4",font=("Ariel", 22, "bold"), corner_radius=label_corner_radius,anchor="e")
    label4.grid(row=2, column=1, padx=(40,0), pady=(10,0))
    label5 = customtkinter.CTkLabel(gelir_gider, text="  Won", fg_color="#ff5090",font=("Ariel", 22, "bold"), corner_radius=label_corner_radius,anchor="e")
    label5.grid(row=2, column=2, padx=(40,0), pady=(10,0))




def AllView(gelir_gider1):
    global gelir_gider
    gelir_gider = gelir_gider1
    labels(gelir_gider)
    gunSec_OptionMenu()
    donemSec_OptionMenu(gelir_gider)
    yilSec_OptionMenu()
    rapor_olusturma_button(gelir_gider)
    donemSec()
    
    gelir_gider.bind("<Configure>", boyut_degisti)
