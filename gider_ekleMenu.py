import customtkinter
import customtkinter
import tkinter as tk
from datetime import datetime
import sqlite3
import gelir_giderMenu
from tkinter import ttk
import threading
from datetime import datetime, timezone, timedelta

conn = sqlite3.connect("gelir_gider.sqlite")
cursor = conn.cursor()

sorgu = """CREATE TABLE IF NOT EXISTS gider_kaydi (id_no INTEGER PRİMARY KEY,gider_detay VARCHAR(40),adet INTEGER,birim_fiyat FLOAT,gider_tarih,gider_saat,toplam_gider FLOAT)"""
cursor.execute(sorgu)


def gider_kaydi_ekle(gider_detay, adet,birim_fiyat,gider_tarih,gider_saat,toplam_gider):
    id_no = None
    veri =  id_no,gider_detay, adet,float(birim_fiyat),gider_tarih,gider_saat,toplam_gider
    # SQLite veritabanına giriş ekleyin
    cursor.execute('''INSERT INTO gider_kaydi VALUES (?,?, ?, ?, ?, ?, ?)''', veri)
    conn.commit()

def verileriTara():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM gider_kaydi')
    veri_sayisi = cursor.fetchone()[0]
    conn.close()
    if veri_sayisi > 0:
        threading.Thread(target=giderleri_getir).start()
    

def giderleri_getir():
    # Tüm gider kayıtlarını getir
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM gider_kaydi ORDER BY id_no')
    gider_kayitlari = cursor.fetchall()
    
    conn.close()
    threading.Thread(target=verileriEkle, args=(gider_kayitlari,)).start()
    
def pencereKapat():
    uyari_Penceresi.destroy()
def pencereyiKapat():
    uyari_Penceresi.destroy()

def kayitTamam():
    global uyari_Penceresi
    turkey_timezone = timezone(timedelta(hours=3))
    now_utc = datetime.now(timezone.utc)
    now_turkey = now_utc.astimezone(turkey_timezone)
    
    gider_detay = giderDetayiEntry.get()
    adet = giderAdetEntry.get()
    birim_fiyat = giderBirimFiyatEntry.get()
    gider_tarih = giderTarihiEntry.get()
    gider_saat = f"{now_turkey.hour:02d}:{now_turkey.minute:02d}:{now_turkey.second:02d}"
    toplam_gider = giderTutariEntry.get()
    
    
    gider_kaydi_ekle(gider_detay, adet,birim_fiyat,gider_tarih,gider_saat,toplam_gider)
    
    if idNoEntry.get() != "" or detayEntry.get() != "" or adetEntry.get() != "" or birimEntry.get() != "" or tarihEntry.get() != "" or tutarEntry.get() != "":
        threading.Thread(target=detayli_Arama_Getir).start()
    else:
        conn = sqlite3.connect("gelir_gider.sqlite")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM gider_kaydi ORDER BY id_no DESC LIMIT 1')
        id_no = cursor.fetchone()[0]
        conn.close()
        default_space = 5
        g_id = str(id_no)
        g_detayi = str(gider_detay)
        g_adet = str(f"{'':<{default_space}}{adet}")
        g_birim_fiyat = str(f"{'':<{default_space}}{birim_fiyat}")
        g_tarihi = str(gider_tarih)
        g_saat = str(f"{'':<{default_space}}{gider_saat}")
        g_toplam_gider = str(f"{'':<{default_space}}{toplam_gider}")
        values =g_id,g_detayi, g_adet,g_birim_fiyat,g_tarihi,g_saat,g_toplam_gider
        table.insert(parent = '',text="1", index = 0 ,values = (values))

    
    giderDetayiEntry.configure(state='disabled')
    giderAdetEntry.configure(state='disabled')
    giderBirimFiyatEntry.configure(state='disabled')
    giderTarihiEntry.configure(state='disabled')
    giderTutariEntry.configure(state='disabled')
    
    kayitEtmeButton.configure(text='Yeni Kayıt İçin Tıkla', fg_color='green',hover_color='green', command=gider_kaydiEkle1)
    new_window_Kapat = customtkinter.CTkButton(new_window, text="Kapat",command=new_window.destroy ,corner_radius=15,width=90, font = ("Ariel", 12, "bold"))
    new_window_Kapat.grid(row=5, column=0,columnspan=2, padx=(0,200), pady=(10,0))#.place(relx=0.05, rely=0.12)
    customtkinter.CTkLabel(new_window, text="      Kayıt Başarılı !      ", corner_radius=label_corner_radius, fg_color='green').grid(row=0, column=1, padx=(0,0), pady=(0,0))

    gelir_giderMenu.donemSec()
    gelir_giderMenu.gunSec_OptionMenu()
    gelir_giderMenu.yilSec_OptionMenu()

def kayit_Uyari():
    global uyari_Penceresi
    uyari_Penceresi = customtkinter.CTkToplevel()
    uyari_Penceresi.title("Hata")
    uyari_Penceresi.minsize(400, 200)
    uyari_Penceresi.resizable(width = False, height = False)
    customtkinter.CTkLabel(uyari_Penceresi, text=f"Hata: {hata_Turu} Bırakılamaz!",font=("Ariel", 15), corner_radius=label_corner_radius, wraplength=380, justify="left").pack(side="top", fill="both", expand=True)
    uyariButton = customtkinter.CTkButton(uyari_Penceresi, text="Tamam",command=pencereKapat,corner_radius=15,width=120,height=40, font = ("Ariel", 12, "bold"))
    uyariButton.pack(side="top", expand=True)
    uyari_Penceresi.grab_set()
    
def gider_kaydiEkle1():
    new_window.destroy()
    gider_kaydiEkle()


def kayitEt():
    global hata_Turu, g_detayi, g_tarihi, g_tutari
    hata_Turu = ""
    g_detayi = giderDetayiEntry.get()
    g_adet = giderAdetEntry.get()
    g_birim_fiyat = giderBirimFiyatEntry.get()
    g_tarihi = giderTarihiEntry.get()
    g_tutari = giderTutariEntry.get()
    if g_detayi == "" or g_tarihi == "" or g_tutari == "" or g_birim_fiyat == "" or g_adet == "":
        if g_detayi == "":
            hata_Turu += "(Gider Detayı Boş)  "
        if g_tarihi == "":
            hata_Turu += "(Gider Tarihi Boş)  "
        if g_tutari == "":
            hata_Turu += "(Gider Tutarı Boş)  "
        if g_birim_fiyat == "":
            hata_Turu += "(Birim Fiyatı Boş)  "
        if g_adet == "":
            hata_Turu += "(Adet Sayısı Boş)  "
        kayit_Uyari()
    else:
        kayitTamam()

# Giriş kutularına fonksiyonlar ekle
def hesapla_birim_fiyat():
    if giderAdetEntry.get() != "":
        adet = int(giderAdetEntry.get())
        if giderTutariEntry.get() != "":
            toplam_tutar = float(giderTutariEntry.get())
            toplam_tutar = round(toplam_tutar / adet, 2)
            giderBirimFiyatEntry.configure(validatecommand=karakterleri_kabul_et)
            giderBirimFiyatEntry.delete(0, "end")
            giderBirimFiyatEntry.insert(0, f"{float(toplam_tutar)}")
            giderBirimFiyatEntry.configure(validatecommand=(new_window.register(validate_birim_fiyat), '%S'))
            

def hesapla_toplam_tutar():
    if giderAdetEntry.get() != "":
        adet = int(giderAdetEntry.get())
        if giderBirimFiyatEntry.get() !="":
            birim_fiyat = float(giderBirimFiyatEntry.get())
            toplam_tutar = round(adet * birim_fiyat, 2)
            giderTutariEntry.configure(validatecommand=karakterleri_kabul_et)
            giderTutariEntry.delete(0, "end")
            giderTutariEntry.insert(0, f"{float(toplam_tutar)}")
            giderTutariEntry.configure(validatecommand=(new_window.register(validate_tutar), '%S'))


def adetKontrol():
    if not giderAdetEntry.get():  # Eğer adet giriş kutusu boşsa
        giderAdetEntry.focus_set()  # Adet giriş kutusuna odaklan
        

def karakterleri_kabul_et(*args):
    # Giriş kutusuna girilen değeri al
    giris = giderBirimFiyatEntry.get()
    
    # Eğer giriş uygunsa True döndür
    # Burada her karakteri kabul ediyoruz, bu nedenle her zaman True döndürüyoruz
    return True

def kayit_ekleLabels(new_window):
    global kayit_ekleLabelsFont
    kayit_ekleLabelsFont = ("Ariel", 15)
    customtkinter.CTkLabel(new_window, text="Gider Detay :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=0, column=0, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
    customtkinter.CTkLabel(new_window, text="Adet :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=1, column=0, padx=(0,0), pady=(5,0))#.place(relx=0.05, rely=0.12)
    customtkinter.CTkLabel(new_window, text="Birim Fiyat :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=2, column=0, padx=(0,0), pady=(5,0))#.place(relx=0.05, rely=0.12)
    customtkinter.CTkLabel(new_window, text="Tarih :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=3, column=0, padx=(0,0), pady=(5,0))#.place(relx=0.05, rely=0.12)
    customtkinter.CTkLabel(new_window, text="Toplam Tutar :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=4, column=0, padx=(0,0), pady=(5,0))#.place(relx=0.05, rely=0.12)


def validate_tutar(char):
    threading.Thread(target=adetKontrol).start()
    threading.Thread(target=hesapla_birim_fiyat).start()
    return char.isdigit() or char == "."
    
def validate_adet(char):
    return char.isdigit()

def validate_birim_fiyat(char):
    threading.Thread(target=adetKontrol).start()
    threading.Thread(target=hesapla_toplam_tutar).start()
    return char.isdigit() or char == "."

def search_in_database(self, term):
        # Burada gerçek bir veritabanı sorgusu yapmalısınız
        # Veritabanınızın türüne ve kullanımına bağlı olarak bu işlemi uygulamalısınız
        # Bu örnekte sadece basit bir kontrol yapısı eklenmiştir
        database = {
            'python': 'Python is a high-level programming language.',
            'tkinter': 'Tkinter is the standard GUI toolkit for Python.',
            'custom': 'You can create custom widgets in Tkinter.'
        }
        similar_sentences = [sentence for key, sentence in database.items() if term in key]
        return similar_sentences


def kayit_ekleEntry(new_window):
    global giderDetayiEntry, giderAdetEntry,giderBirimFiyatEntry, giderTarihiEntry, giderTutariEntry
    entryWidth = 250
    bugunun_tarihi = datetime.today().date()
    
    giderDetayiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Gider Detayı",width = entryWidth)
    giderDetayiEntry.grid(row=0, column=1, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
    giderAdetEntry = customtkinter.CTkEntry(new_window, placeholder_text="Adet",width = entryWidth ,validate="key",validatecommand=(new_window.register(validate_adet), '%S'))
    giderAdetEntry.grid(row=1, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    giderBirimFiyatEntry = customtkinter.CTkEntry(new_window, placeholder_text="Birim Fiyat",width = entryWidth, validate= "key",validatecommand=(new_window.register(validate_birim_fiyat), '%S'))
    giderBirimFiyatEntry.grid(row=2, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    giderTarihiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Tarih", width = entryWidth)
    giderTarihiEntry.grid(row=3, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    giderTutariEntry = customtkinter.CTkEntry(new_window,validate="key",validatecommand=(new_window.register(validate_tutar), '%S'),  width = entryWidth)
    giderTutariEntry.grid(row=4, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    giderTarihiEntry.insert(0, bugunun_tarihi)
    

def gider_kaydiEkle():
    global new_window, kayitEtmeButton
    # Yeni pencere oluştur
    new_window = customtkinter.CTkToplevel()
    new_window.title("Gider Kaydı Ekle")
    new_window.minsize(400, 300)
    kayit_ekleLabels(new_window)
    kayit_ekleEntry(new_window)
    kayitEtmeButton = customtkinter.CTkButton(new_window, text="Kayıt Et",command=kayitEt,corner_radius=15,width=90, font = ("Ariel", 12, "bold"))
    kayitEtmeButton.grid(row=5, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    new_window.resizable(width = False, height = False)
    new_window.grab_set()



def gider_ekleButton(gider_ekle):
    gider_eklemeButton = customtkinter.CTkButton(gider_ekle, text="Gider Kayıdı Ekle",command=gider_kaydiEkle,corner_radius=15, font = ("Ariel", 12, "bold"))
    gider_eklemeButton.grid(row=0, column=3,columnspan=2, padx=(0,0), pady=(25,25))

def labels(gider_ekle):
    customtkinter.CTkLabel(gider_ekle, text="ID No", fg_color=label_color, width=10,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.005, rely=0.12)#.grid(row=1, column=0, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Detay", fg_color=label_color, width=300,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.10, rely=0.12)#.grid(row=1, column=1, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Adet", fg_color=label_color, width=75,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.45, rely=0.12)#.grid(row=1, column=2, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Birim Fiyat", fg_color=label_color, width=100,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.57, rely=0.12)#.grid(row=1, column=2, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Tarih", fg_color=label_color, width=50,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.70, rely=0.12)#.grid(row=1, column=2, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Saat", fg_color=label_color, width=50,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.80, rely=0.12)#.grid(row=1, column=2, padx=(0,0), pady=(50,0))
    customtkinter.CTkLabel(gider_ekle, text="Toplam Tutar", fg_color=label_color, width=100,font=label_font, height=10, corner_radius=label_corner_radius).place(relx=0.90, rely=0.12)#.grid(row=1, column=2, padx=(0,0), pady=(50,0))


def item_select(_):
    for i in table.selection():
        new_window = customtkinter.CTkToplevel()
        new_window.title("Gider Kaydı Detayı")
        new_window.minsize(400, 300)
        kayit_ekleLabels(new_window)
        customtkinter.CTkLabel(new_window, text="Id No :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=0, column=0, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
        veriler = table.item(i)['values']
        kayit_detay_entry(new_window,veriler)
        kayit_detay_button(new_window)
        new_window.grab_set()
    
def kayit_detay_button(new_window):
    kayit_guncelle_button = customtkinter.CTkButton(new_window, text="Güncelle",state='disabled',hover_color='green',fg_color='green',corner_radius=15, font = ("Ariel", 12, "bold"))
    kayit_guncelle_button.grid(row=5, column=0,columnspan=2, padx=(100,0), pady=(10,0))
    kayit_kapat_button = customtkinter.CTkButton(new_window, text="Kapat",hover_color='red',command=new_window.destroy,fg_color='red',corner_radius=15, font = ("Ariel", 12, "bold"))
    kayit_kapat_button.grid(row=5, column=0,columnspan=2, padx=(0,100), pady=(10,0))
    
def kayit_detay_entry(new_window,veriler):
    global kayitDetayiEntry, kayitAdetEntry,kayitBirimFiyatEntry, kayitTarihiEntry, kayitTutariEntry
    entryWidth = 250
    bugunun_tarihi = datetime.today().date()
    
    kayitIdNoEntry = customtkinter.CTkEntry(new_window, placeholder_text="Id No",width = entryWidth)
    kayitIdNoEntry.grid(row=0, column=1, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    kayitIdNoEntry.insert(0,veriler[0])
    kayitIdNoEntry.configure(state='disabled')
    
    kayitDetayiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Gider Detayı",width = entryWidth)
    kayitDetayiEntry.grid(row=0, column=1, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
    kayitDetayiEntry.insert(0,veriler[1])
    kayitAdetEntry = customtkinter.CTkEntry(new_window, placeholder_text="Adet",width = entryWidth)
    kayitAdetEntry.grid(row=1, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    kayitAdetEntry.insert(0,veriler[2])
    kayitBirimFiyatEntry = customtkinter.CTkEntry(new_window, placeholder_text="Birim Fiyat",width = entryWidth)
    kayitBirimFiyatEntry.grid(row=2, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    kayitBirimFiyatEntry.insert(0,veriler[3].strip())
    kayitTarihiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Tarih", width = entryWidth)
    kayitTarihiEntry.grid(row=3, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    
    kayitTutariEntry = customtkinter.CTkEntry(new_window,validate="key", width = entryWidth)
    kayitTutariEntry.grid(row=4, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    kayitTutariEntry.insert(0,veriler[6].strip())
    kayitTarihiEntry.insert(0, bugunun_tarihi)
        

def giderDetay(gider_ekle):
    global table, columns, treeviewStyle
    screen_width = gider_ekle.winfo_screenwidth()
    screen_height = gider_ekle.winfo_screenheight()

    treeviewStyle = ttk.Style()
    treeviewStyle.configure("Custom.Treeview", font=("Arial", 16))
    
    columns = ("id_no","detay","adet","birim_fiyat","tarih","saat","toplam_Tutar")
    columns_text = ("ID No","Detay","Adet","Birim Fiyat","Tarih","Saat","Toplam Tutar")
    table = ttk.Treeview(gider_ekle, columns =  columns, show = 'headings', style="Custom.Treeview", height=30)
    table.grid(row=2, column=0,columnspan=10, padx=(0,0), pady=(0,0))
    
    # create CTk scrollbar
    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(gider_ekle, command=table.yview)
    ctk_textbox_scrollbar.grid(row=2, column=10, sticky="ns", pady=(10,0))

    # connect textbox scroll event to CTk scrollbar
    table.configure(yscrollcommand=ctk_textbox_scrollbar.set)
    
    table.heading(columns[0], text=columns_text[0], anchor='center')
    table.heading(columns[1], text=columns_text[1], anchor='center')
    table.heading(columns[2], text=columns_text[2], anchor='center')
    table.heading(columns[3], text=columns_text[3], anchor='center')
    table.heading(columns[4], text=columns_text[4], anchor='center')
    table.heading(columns[5], text=columns_text[5], anchor='center')
    table.heading(columns[6], text=columns_text[6], anchor='center')
    
    table.bind('<<TreeviewSelect>>', item_select)


def verileriEkle(veriler):
    table_values = table.get_children()
    if table_values:
        table.delete(*table_values)
    
    for gider in veriler:
        g_id, g_detayi,g_adet,g_birim_fiyat, g_tarihi, g_saat, g_toplam_gider = gider[0], gider[1], gider[2], gider[3], gider[4], gider[5], gider[6]
        default_space = 5
        g_id = str(g_id)
        g_detayi = str(g_detayi)
        g_adet = str(f"{'':<{default_space}}{g_adet}")
        g_birim_fiyat = str(f"{'':<{default_space}}{g_birim_fiyat}")
        g_tarihi = str(g_tarihi)
        g_saat = str(f"{'':<{default_space}}{g_saat}")
        g_toplam_gider = str(f"{'':<{default_space}}{g_toplam_gider}")

        values = g_id, g_detayi,g_adet,g_birim_fiyat, g_tarihi, g_saat, g_toplam_gider
        
        table.insert(parent = '',text="1", index = 0 ,values = (values))

def validate_idNoEnrty(char):
    threading.Thread(target=detayli_Arama_Getir).start()
    return char.isdigit() 
    
def validate_detayEntry(char):
    threading.Thread(target=detayli_Arama_Getir).start()
    return char.isprintable()
    
def validate_adetEntry(char):
    threading.Thread(target=detayli_Arama_Getir).start()
    return char.isdigit() 

def validate_birimEntry(char):
    threading.Thread(target=detayli_Arama_Getir).start()
    return char.isdigit() or char == "."

def validate_tarihEntry(char):
    threading.Thread(target=detayli_Arama_Getir).start()
    return char.isdigit() or char == "-"
    
def detayli_Arama(gider_ekle):
    global idNoEntry, detayEntry, adetEntry, birimEntry, tarihEntry, tutarEntry
    idNoEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_idNoEnrty), '%S'))
    idNoEntry.grid(row=1, column=0, padx=(0,30), pady=(0,0))#.place(relx=0.05, rely=0.12)
    detayEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_detayEntry), '%S'))
    detayEntry.grid(row=1, column=1, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    adetEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_adetEntry), '%S'))
    adetEntry.grid(row=1, column=2, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    birimEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_birimEntry), '%S'))
    birimEntry.grid(row=1, column=3, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    tarihEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_tarihEntry), '%S'))
    tarihEntry.grid(row=1, column=4, padx=(0,30), pady=(0,0))#.place(relx=0.05, rely=0.12)
    tutarEntry = customtkinter.CTkEntry(gider_ekle, validate="key",validatecommand=(gider_ekle.register(validate_adetEntry), '%S'))
    tutarEntry.grid(row=1, column=9, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)

def detayli_Arama_Getir():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    if idNoEntry.get() != "" or detayEntry.get() != "" or adetEntry.get() != "" or birimEntry.get() != "" or tarihEntry.get() != "" or tutarEntry.get() != "":
        if idNoEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE id_no LIKE ?"
            parametreler = (f'%{idNoEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            idNoValues = cursor.fetchall()
            
            if idNoValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(idNoValues,)).start()
            
        if detayEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE gider_detay LIKE ?"
            parametreler = (f'%{detayEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            detayValues = cursor.fetchall()
            if detayValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(detayValues,)).start()
            
        if adetEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE adet LIKE ?"
            parametreler = (f'%{adetEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            adetValues = cursor.fetchall()
            if adetValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(adetValues,)).start()
            
        if birimEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE birim_fiyat LIKE ?"
            parametreler = (f'{birimEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            birimValues = cursor.fetchall()
            if birimValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(birimValues,)).start()
            
        if tarihEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE gider_tarih LIKE ?"
            parametreler = (f'%{tarihEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            tarihValues = cursor.fetchall()
            if tarihValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(tarihValues,)).start()
            
        if tutarEntry.get() != "":
            sorgu = "SELECT * FROM gider_kaydi WHERE toplam_gider LIKE ?"
            parametreler = (f'%{tutarEntry.get()}%',)
            cursor = conn.cursor()
            cursor.execute(sorgu, parametreler)
            tutarValues = cursor.fetchall()
            if tutarValues is None:
                print("Değer Bulunamadı")
            else:
                conn.close()
                threading.Thread(target=verileriEkle, args=(tutarValues,)).start()
            
    else:
        conn.close()
        threading.Thread(target=verileriTara).start()
        
    
def boyut_degisti(event):
    label_width = int(event.width * 0.15)
    label_height = int(event.height * 0.035)
    
    idNoEntry.configure(width=event.width * 0.03)
    detayEntry.configure(width=event.width * 0.2)
    adetEntry.configure(width=event.width * 0.04)
    birimEntry.configure(width=event.width * 0.04)
    tarihEntry.configure(width=event.width * 0.06)
    tutarEntry.configure(width=event.width * 0.08)

    treeviewStyle.configure('Custom.Treeview', rowheight=int(event.height*0.028))

    table.column(columns[0], minwidth=int(event.width * 0.04), width=int(event.width * 0.04))
    table.column(columns[1], minwidth=int(event.width * 0.3), width=int(event.width * 0.3))
    table.column(columns[2], minwidth=int(event.width * 0.06), width=int(event.width * 0.06))
    table.column(columns[3], minwidth=int(event.width * 0.08), width=int(event.width * 0.08))
    table.column(columns[4], minwidth=int(event.width * 0.08), width=int(event.width * 0.08))
    table.column(columns[5], minwidth=int(event.width * 0.1), width=int(event.width * 0.1))
    table.column(columns[6], minwidth=int(event.width * 0.1), width=int(event.width * 0.1))


def AllView(gider_ekle):
    global label_width, label_height, label_corner_radius, label_font, label_color
        #Label boyutları
    label_width=300
    label_height=25
    label_corner_radius=3
    label_font = ("Ariel", 15, "bold")
    label_color = "#1ab394"

    detayli_Arama(gider_ekle)
    giderDetay(gider_ekle)
    gider_ekleButton(gider_ekle)
    
    verileriTara()
    
    gider_ekle.bind("<Configure>", boyut_degisti)
