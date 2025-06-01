import sqlite3


def get_Data():
    conn = sqlite3.connect("gelir_gider.sqlite")
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM gider_kaydi ORDER BY id_no')
    gider_kayitlari = cursor.fetchall()

    liste = []
    for gider in gider_kayitlari:
        liste.append(gider)
    return liste

