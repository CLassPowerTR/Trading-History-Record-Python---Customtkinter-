import customtkinter
import tkinter as tk
from datetime import datetime
import sqlite3
import gelir_giderMenu
import threading
from tkinter import ttk
from datetime import datetime, timezone, timedelta
import time
global dbName


dbName = "gelir_gider.sqlite"

conn = sqlite3.connect(dbName)
cursor = conn.cursor()

sorgu = """CREATE TABLE IF NOT EXISTS gelir_kaydi (id_no,gelir_detay,adet,birim_fiyat,gelir_tarih,gelir_saat,toplam_gelir)"""
cursor.execute(sorgu)
conn.close()


def sqlQuery(execute, veri=None):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    if veri == None:
        cursor.execute(execute)
    else:
        cursor.execute(execute,veri)
    conn.commit()
    conn.close()
    
def sqlQueryFetchone(execute):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    cursor.execute(execute)
    veri_sayisi = cursor.fetchone()[0]
    conn.close()
    return veri_sayisi
    
def sqlQueryFetchall(execute, veri=None):
    conn = sqlite3.connect(dbName)
    cursor = conn.cursor()
    if veri == None:
        cursor.execute(execute)
    else:
        cursor.execute(execute, veri)
    gelir_kayitlari = cursor.fetchall()
    conn.close()
    return gelir_kayitlari
  
def gelir_kaydi_ekle(gelir_detay, adet,birim_fiyat,gelir_tarih,gelir_saat,toplam_gelir):
    id_no = None
    veri = id_no, gelir_detay, adet,float(birim_fiyat),gelir_tarih,gelir_saat,toplam_gelir
    # SQLite veritabanına giriş ekleyin
    execute = '''INSERT INTO gelir_kaydi VALUES (?, ? , ? , ?, ?, ?,? )'''
    sqlQuery(execute, (veri))

def verileriTara():
    execute = 'SELECT COUNT(*) FROM gelir_kaydi'
    veri_sayisi = sqlQueryFetchone(execute)
    if veri_sayisi > 0:
        threading.Thread(target=gelirleri_getir).start()
    
    
def gelirleri_getir():
    # Tüm gelir kayıtlarını getir
    execute = 'SELECT * FROM gelir_kaydi ORDER BY gelir_tarih'
    gelir_kayitlari = sqlQueryFetchall(execute)
    threading.Thread(target=verileriEkle, args=(gelir_kayitlari,)).start()

def pencereKapat():
    uyari_Penceresi.destroy()
def pencereyiKapat():
    uyari_Penceresi.destroy()
    

def kayitTamam():
    global uyari_Penceresi
    turkey_timezone = timezone(timedelta(hours=3))
    now_utc = datetime.now(timezone.utc)
    now_turkey = now_utc.astimezone(turkey_timezone)
    
    gelir_detay = gelirDetayiEntry.get()
    adet = gelirAdetEntry.get()
    birim_fiyat = gelirBirimFiyatEntry.get()
    gelir_tarih = gelirTarihiEntry.get()
    gelir_saat = f"{now_turkey.hour:02d}:{now_turkey.minute:02d}:{now_turkey.second:02d}"
    toplam_gelir = gelirTutariEntry.get()
    
    gelir_kaydi_ekle(gelir_detay, adet,birim_fiyat,gelir_tarih,gelir_saat,toplam_gelir)
    
    
    if idNoEntry.get() != "" or detayEntry.get() != "" or adetEntry.get() != "" or birimEntry.get() != "" or tarihEntry.get() != "" or tutarEntry.get() != "":
        threading.Thread(target=detayli_Arama_Getir).start()
    else:
        execute = 'SELECT * FROM gelir_kaydi ORDER BY id_no DESC LIMIT 1'
        id_no = sqlQueryFetchone(execute)
        default_space = 5
        g_id = str(id_no)
        g_detayi = str(gelir_detay)
        g_adet = str(f"{'':<{default_space}}{adet}")
        g_birim_fiyat = str(f"{'':<{default_space}}{birim_fiyat}")
        g_tarihi = str(gelir_tarih)
        g_saat = str(f"{'':<{default_space}}{gelir_saat}")
        g_toplam_gider = str(f"{'':<{default_space}}{toplam_gelir}")
        values =g_id,g_detayi, g_adet,float(g_birim_fiyat),g_tarihi,g_saat,g_toplam_gider
        table.insert(parent = '',text="1",iid=g_id, index = 0 ,values = (values))
    
    gelirDetayiEntry.configure(state='disabled')
    gelirAdetEntry.configure(state='disabled')
    gelirBirimFiyatEntry.configure(state='disabled')
    gelirTarihiEntry.configure(state='disabled')
    gelirTutariEntry.configure(state='disabled')
    
    kayitEtmeButton.configure(text='Yeni Kayıt İçin Tıkla', fg_color='green',hover_color='green', command=gelir_kaydiEkle1)
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


def gelir_kaydiEkle1():
    new_window.destroy()
    gelir_kaydiEkle()

def kayitEt():
    global hata_Turu, g_detayi, g_tarihi, g_tutari, x
    hata_Turu = ""
    g_detayi = gelirDetayiEntry.get()
    g_adet = gelirAdetEntry.get()
    g_birim_fiyat = gelirBirimFiyatEntry.get()
    g_tarihi = gelirTarihiEntry.get()
    g_tutari = gelirTutariEntry.get()
    if g_detayi == "" or g_tarihi == "" or g_tutari == "" or g_birim_fiyat == "" or g_adet == "":
        if g_detayi == "":
            hata_Turu += "(Gelir Detayı Boş)  "
        if g_tarihi == "":
            hata_Turu += "(Gelir Tarihi Boş)  "
        if g_tutari == "":
            hata_Turu += "(Gelir Tutarı Boş)  "
        if g_birim_fiyat == "":
            hata_Turu += "(Birim Fiyatı Boş)  "
        if g_adet == "":
            hata_Turu += "(Adet Sayısı Boş)  "
        kayit_Uyari()
    else:
        kayitTamam()

# Giriş kutularına fonksiyonlar ekle
def hesapla_birim_fiyat():
    if gelirAdetEntry.get() != "":
        adet = int(gelirAdetEntry.get())
        if gelirTutariEntry.get() != "":
            toplam_tutar = float(gelirTutariEntry.get())
            toplam_tutar = round(toplam_tutar / adet, 2)
            gelirBirimFiyatEntry.configure(validatecommand=karakterleri_kabul_et)
            gelirBirimFiyatEntry.delete(0, "end")
            gelirBirimFiyatEntry.insert(0, f"{float(toplam_tutar)}")
            gelirBirimFiyatEntry.configure(validatecommand=(new_window.register(validate_birim_fiyat), '%S'))
            

def hesapla_toplam_tutar():
    if gelirAdetEntry.get() != "":
        adet = int(gelirAdetEntry.get())
        if gelirBirimFiyatEntry.get() !="":
            birim_fiyat = float(gelirBirimFiyatEntry.get())
            toplam_tutar = round(adet * birim_fiyat, 2)
            toplam_tutar1 = int(toplam_tutar - int(toplam_tutar))
            gelirTutariEntry.configure(validatecommand=karakterleri_kabul_et)
            gelirTutariEntry.delete(0, "end")
            gelirTutariEntry.insert(0, f"{float(toplam_tutar)}")
            gelirTutariEntry.configure(validatecommand=(new_window.register(validate_tutar), '%S'))


def adetKontrol():
    if not gelirAdetEntry.get():  # Eğer adet giriş kutusu boşsa
        gelirAdetEntry.focus_set()  # Adet giriş kutusuna odaklan
        

def karakterleri_kabul_et(*args):
    # Giriş kutusuna girilen değeri al
    giris = gelirBirimFiyatEntry.get()
    
    # Eğer giriş uygunsa True döndür
    # Burada her karakteri kabul ediyoruz, bu nedenle her zaman True döndürüyoruz
    return True


def kayit_ekleLabels(new_window):
    
    kayit_ekleLabelsFont = ("Ariel", 15)
    customtkinter.CTkLabel(new_window, text="Gelir Detay :",font=kayit_ekleLabelsFont, corner_radius=label_corner_radius).grid(row=0, column=0, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
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

def kayit_ekleEntry(new_window):
    global gelirDetayiEntry, gelirAdetEntry,gelirBirimFiyatEntry, gelirTarihiEntry, gelirTutariEntry
    entryWidth = 250
    bugunun_tarihi = datetime.today().date()
    
    gelirDetayiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Gelir Detayı",width = entryWidth)
    gelirDetayiEntry.grid(row=0, column=1, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
    gelirAdetEntry = customtkinter.CTkEntry(new_window, placeholder_text="Adet",width = entryWidth ,validate="key",validatecommand=(new_window.register(validate_adet), '%S'))
    gelirAdetEntry.grid(row=1, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    gelirBirimFiyatEntry = customtkinter.CTkEntry(new_window, placeholder_text="Birim Fiyat",width = entryWidth, validate= "key",validatecommand=(new_window.register(validate_birim_fiyat), '%S'))
    gelirBirimFiyatEntry.grid(row=2, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    gelirTarihiEntry = customtkinter.CTkEntry(new_window, placeholder_text="Tarih", width = entryWidth)
    gelirTarihiEntry.grid(row=3, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    gelirTutariEntry = customtkinter.CTkEntry(new_window,validate="key",validatecommand=(new_window.register(validate_tutar), '%S'),  width = entryWidth)
    gelirTutariEntry.grid(row=4, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    gelirTarihiEntry.insert(0, bugunun_tarihi)
    
    gelirBirimFiyatEntry.bind("<FocusIn>", adetKontrol())
    gelirTutariEntry.bind("<FocusIn>", adetKontrol())

    

def gelir_kaydiEkle():
    global new_window, kayitEtmeButton
    # Yeni pencere oluştur
    new_window = customtkinter.CTkToplevel()
    new_window.title("Gelir Kaydı Ekle")
    new_window.minsize(400, 300)
    kayit_ekleLabels(new_window)
    kayit_ekleEntry(new_window)
    kayitEtmeButton = customtkinter.CTkButton(new_window, text="Kayıt Et",command=kayitEt,corner_radius=15, font = ("Ariel", 12, "bold"))
    kayitEtmeButton.grid(row=5, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    new_window.resizable(width = False, height = False)
    new_window.grab_set()


def gelir_ekleButton(gelir_ekle):
    gelir_eklemeButton = customtkinter.CTkButton(gelir_ekle, text="Gelir Kayıdı Ekle",command=gelir_kaydiEkle,corner_radius=15, font = ("Ariel", 12, "bold"))
    gelir_eklemeButton.grid(row=0, column=3,columnspan=2, padx=(0,0), pady=(25,25))



def item_select(_):
    global veriler, dataUpdateWindow
    kayitDetayFont = ("Ariel", 15)
    for i in table.selection():
        dataUpdateWindow = customtkinter.CTkToplevel()
        dataUpdateWindow.title("Gelir Kaydı Detayı")
        dataUpdateWindow.minsize(400, 300)
        kayit_ekleLabels(dataUpdateWindow)
        customtkinter.CTkLabel(dataUpdateWindow, text="Id No :",font=kayitDetayFont, corner_radius=label_corner_radius).grid(row=0, column=0, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
        veriler = table.item(i)['values']
        kayit_detay_entry(dataUpdateWindow)
        kayit_detay_button()
        dataUpdateWindow.grab_set()

def update_datas():
    # Şu anki zamanı al
    su_an = datetime.now()
    # Saati saat.dakika formatında yazdır
    zaman = su_an.strftime("%H:%M:%S")
    newDatas = [kayitDetayiEntry.get(), kayitAdetEntry.get(),kayitBirimFiyatEntry.get(),kayitTutariEntry.get()]
    oldDatas = [veriler[1],veriler[2],veriler[3],veriler[6]]
    count = 0
    for i in oldDatas:
        if str(i).strip() != newDatas[count]:
            
            veri = kayitDetayiEntry.get(), kayitAdetEntry.get(),kayitBirimFiyatEntry.get(), kayitTarihiEntry.get(),zaman, kayitTutariEntry.get(),kayitIdNoEntry.get()
            execute = '''UPDATE gelir_kaydi SET gelir_detay = ?, adet = ?, birim_fiyat = ?,gelir_tarih = ?,gelir_saat = ?, toplam_gelir = ?  WHERE id_no=?;'''
            sqlQuery(execute,veri)
            threading.Thread(target=veri_guncelle()).start()
            
            break
        else:
            #print(f"eski veri: {i}\nyeni veri: {newDatas[count]}")
            pass
        count += 1
        
   

def veri_guncelle():
    execute = '''SELECT * FROM gelir_kaydi WHERE id_no = ?;'''
    veriyi_guncelle = sqlQueryFetchall(execute,(kayitIdNoEntry.get(),))
    table.item(kayitIdNoEntry.get(),values=veriyi_guncelle[0])
    dataUpdateWindow.destroy()
    
def delete_data():
    execute = '''DELETE FROM gelir_kaydi WHERE id_no = ?;'''
    sqlQuery(execute, (kayitIdNoEntry.get(),))
    table.delete(kayitIdNoEntry.get())
    dataUpdateWindow.destroy()

def kayit_detay_button():
    detayButtonWidth = 70
    kayit_guncelle_button = customtkinter.CTkButton(dataUpdateWindow, width = detayButtonWidth ,text="Güncelle",command = update_datas,hover_color='green',fg_color='green',corner_radius=15, font = ("Ariel", 12, "bold"))
    kayit_guncelle_button.grid(row=5, column=0,columnspan=1, padx=(0,0), pady=(10,0))
    kayit_kapat_button = customtkinter.CTkButton(dataUpdateWindow,width = detayButtonWidth , text="Kapat",hover_color='red',command=dataUpdateWindow.destroy,fg_color='red',corner_radius=15, font = ("Ariel", 12, "bold"))
    kayit_kapat_button.grid(row=5, column=1, columnspan=2, padx=(120,0), pady=(10,0))
    kayit_sil_button = customtkinter.CTkButton(dataUpdateWindow,width = detayButtonWidth ,command = delete_data, text="Sil",hover_color='red',fg_color='red',corner_radius=15, font = ("Ariel", 12, "bold"))
    kayit_sil_button.grid(row=5, column=1, columnspan=1, padx=(0,120), pady=(10,0))
    
def kayit_detay_entry(dataUpdateWindow):
    global kayitIdNoEntry,kayitDetayiEntry, kayitAdetEntry,kayitBirimFiyatEntry, kayitTarihiEntry, kayitTutariEntry
    entryWidth = 250
    bugunun_tarihi = datetime.today().date()
    
    kayitIdNoEntry = customtkinter.CTkEntry(dataUpdateWindow, placeholder_text="Id No",width = entryWidth)
    kayitIdNoEntry.grid(row=0, column=1, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    kayitIdNoEntry.insert(0,veriler[0])
    kayitIdNoEntry.configure(state='disabled')
    
    kayitDetayiEntry = customtkinter.CTkEntry(dataUpdateWindow, placeholder_text="Gider Detayı",width = entryWidth)
    kayitDetayiEntry.grid(row=0, column=1, padx=(0,0), pady=(70,0))#.place(relx=0.05, rely=0.12)
    kayitDetayiEntry.insert(0,veriler[1])
    kayitAdetEntry = customtkinter.CTkEntry(dataUpdateWindow, placeholder_text="Adet",width = entryWidth)
    kayitAdetEntry.grid(row=1, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    kayitAdetEntry.insert(0,veriler[2])
    kayitBirimFiyatEntry = customtkinter.CTkEntry(dataUpdateWindow, placeholder_text="Birim Fiyat",width = entryWidth)
    kayitBirimFiyatEntry.grid(row=2, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)

    kayitBirimFiyatEntry.insert(0,veriler[3].strip())

    kayitTarihiEntry = customtkinter.CTkEntry(dataUpdateWindow, placeholder_text="Tarih", width = entryWidth)
    kayitTarihiEntry.grid(row=3, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    
    kayitTutariEntry = customtkinter.CTkEntry(dataUpdateWindow,validate="key", width = entryWidth)
    kayitTutariEntry.grid(row=4, column=1, padx=(0,0), pady=(10,0))#.place(relx=0.05, rely=0.12)
    kayitTutariEntry.insert(0,veriler[6].strip())
    kayitTarihiEntry.insert(0, bugunun_tarihi)

def gelirDetay(gelir_ekle):
    global table, treeviewStyle, columns
    screen_width = gelir_ekle.winfo_screenwidth()
    screen_height = gelir_ekle.winfo_screenheight()

    treeviewStyle = ttk.Style()
    treeviewStyle.configure("Custom.Treeview", font=("Arial", 16),background="lightgray", foreground="black",rowheight=25, fieldbackground="white")
    
    columns = ("id_no","detay","adet","birim_fiyat","tarih","saat","toplam_Tutar")
    columns_text = ("ID No","Detay","Adet","Birim Fiyat","Tarih","Saat","Toplam Tutar")
    table = ttk.Treeview(gelir_ekle, columns =  columns, show = 'headings',style="Custom.Treeview", height=30)
    table.grid(row=2, column=0,columnspan=10, padx=(0,0), pady=(0,0))
    
    # create CTk scrollbar
    ctk_textbox_scrollbar = customtkinter.CTkScrollbar(gelir_ekle, command=table.yview)
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
    
    for gelir in veriler:
        g_id, g_detayi,g_adet,g_birim_fiyat, g_tarihi, g_saat, g_toplam_gelir = gelir[0], gelir[1], gelir[2], gelir[3], gelir[4], gelir[5], gelir[6]
        default_space = 5
        g_id = str(g_id)
        g_detayi = str(g_detayi)
        g_adet = str(f"{'':<{default_space}}{g_adet}")
        g_birim_fiyat = str(f"{'':<{default_space}}{g_birim_fiyat}")
        g_tarihi = str(g_tarihi)
        g_saat = str(f"{'':<{default_space}}{g_saat}")
        g_toplam_gelir = str(f"{'':<{default_space}}{g_toplam_gelir}")

        values = g_id, g_detayi,g_adet,g_birim_fiyat, g_tarihi, g_saat, g_toplam_gelir
        
        table.insert(parent = '',text="1",iid=g_id, index = 0 ,values = (values))
    

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

def detayli_Arama(gelir_ekle):
    global idNoEntry, detayEntry, adetEntry, birimEntry, tarihEntry, tutarEntry
    idNoEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_idNoEnrty), '%S'))
    idNoEntry.grid(row=1, column=0, padx=(0,30), pady=(0,0))#.place(relx=0.05, rely=0.12)
    detayEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_detayEntry), '%S'))
    detayEntry.grid(row=1, column=1, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    adetEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_adetEntry), '%S'))
    adetEntry.grid(row=1, column=2, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    birimEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_birimEntry), '%S'))
    birimEntry.grid(row=1, column=3, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)
    tarihEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_tarihEntry), '%S'))
    tarihEntry.grid(row=1, column=4, padx=(0,30), pady=(0,0))#.place(relx=0.05, rely=0.12)
    tutarEntry = customtkinter.CTkEntry(gelir_ekle, validate="key",validatecommand=(gelir_ekle.register(validate_birimEntry), '%S'))
    tutarEntry.grid(row=1, column=9, padx=(0,0), pady=(0,0))#.place(relx=0.05, rely=0.12)

def detayli_Arama_Getir():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()
    if idNoEntry.get() != "" or detayEntry.get() != "" or adetEntry.get() != "" or birimEntry.get() != "" or tarihEntry.get() != "" or tutarEntry.get() != "":
        if idNoEntry.get() != "":
            sorgu = "SELECT * FROM gelir_kaydi WHERE id_no LIKE ?"
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
            sorgu = "SELECT * FROM gelir_kaydi WHERE gelir_detay LIKE ?"
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
            sorgu = "SELECT * FROM gelir_kaydi WHERE adet LIKE ?"
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
            sorgu = "SELECT * FROM gelir_kaydi WHERE birim_fiyat LIKE ?"
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
            sorgu = "SELECT * FROM gelir_kaydi WHERE gelir_tarih LIKE ?"
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
            sorgu = "SELECT * FROM gelir_kaydi WHERE toplam_gelir LIKE ?"
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
    
    idNoEntry.configure(width=int(event.width * 0.03))
    detayEntry.configure(width=int(event.width * 0.2))
    adetEntry.configure(width=int(event.width * 0.04))
    birimEntry.configure(width=int(event.width * 0.04))
    tarihEntry.configure(width=int(event.width * 0.06))
    tutarEntry.configure(width=int(event.width * 0.08))
    
    treeviewStyle.configure('Custom.Treeview', rowheight=int(event.height*0.028))
    
    table.column(columns[0], minwidth=int(event.width * 0.04), width=int(event.width * 0.04))
    table.column(columns[1], minwidth=int(event.width * 0.3), width=int(event.width * 0.3))
    table.column(columns[2], minwidth=int(event.width * 0.06), width=int(event.width * 0.06))
    table.column(columns[3], minwidth=int(event.width * 0.08), width=int(event.width * 0.08))
    table.column(columns[4], minwidth=int(event.width * 0.08), width=int(event.width * 0.08))
    table.column(columns[5], minwidth=int(event.width * 0.1), width=int(event.width * 0.1))
    table.column(columns[6], minwidth=int(event.width * 0.1), width=int(event.width * 0.1))

def AllView(gelir_ekle):
    global label_width, label_height, label_corner_radius, label_font, label_color
        #Label boyutları
    label_width=300
    label_height=25
    label_corner_radius=3
    label_font = ("Ariel", 15, "bold")
    label_color = "#1ab394"
    

    detayli_Arama(gelir_ekle)
    gelirDetay(gelir_ekle)
    gelir_ekleButton(gelir_ekle)
    
    verileriTara()
    
    gelir_ekle.bind("<Configure>", boyut_degisti)