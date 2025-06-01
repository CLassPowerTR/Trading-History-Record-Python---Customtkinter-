import sqlite3

vt = sqlite3.connect('gelir_gider.sqlite')
im = vt.cursor()


sorgu = """CREATE TABLE IF NOT EXISTS gelir_kaydi (gelir_detay, gelir_tarih, gelir_tutar)"""

veri_gir = """INSERT INTO gelir_kaydi VALUES ('Vaneda Bot', '28-11-2023', '2500')"""


im.execute(sorgu)
im.execute(veri_gir)



vt.commit()
vt.close()

import sqlite3

with sqlite3.connect('gelir_gider.sqlite') as vt:
    im = vt.cursor()

    veriler = [('Vaneda Bot', '28-11-2023', '2500')]

    im.execute("""CREATE TABLE IF NOT EXISTS gelir_kaydi (gelir_detay, gelir_tarih, gelir_tutar)""")

    for veri in veriler:
        im.execute("""INSERT INTO gelir_kaydi VALUES
            (?, ?, ?)""", veri)

    vt.commit()