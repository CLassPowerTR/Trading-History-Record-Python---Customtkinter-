import customtkinter as ctk
from tkcalendar import Calendar
import locale

# Türkçe dil ayarı
locale.setlocale(locale.LC_TIME, "tr_TR.utf8")

class TurkishCalendar(Calendar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Türkçe gün ve ay isimleri
        self.day_abbr = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
        self.month_name = ["", "Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]

        # formatyearpage'i özelleştir
        self.formatyearpage = self.custom_format_year_page

    def custom_format_year_page(self, theyear, wname, fwday, showweek):
        out = self.formatyear(theyear, 2, 1, 1, 3, 1, 1, 3, 1, fwday, showweek)
        return out

class CTkDateEntry(ctk.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.entry = ctk.CTkEntry(self, validate="key", validatecommand=(self.register(self.validate_tarih), '%S'))
        self.entry.grid(row=0, column=0, padx=(0, 5))

        self.button = ctk.CTkButton(self, text="...", command=self.show_calendar)
        self.button.grid(row=0, column=1)

    def validate_tarih(self, char):
        return char.isdigit() or char == "-"

    def show_calendar(self):
        top = ctk.CTkToplevel(self)
        cal = TurkishCalendar(top, font="Arial 14", selectmode="day")
        cal.pack(fill="both", expand=True)
        cal.bind("<<CalendarSelected>>", lambda event, entry=self.entry, top=top: self.update_entry(entry, cal, top))

    def update_entry(self, entry, calendar, top):
        selected_date = calendar.get_date()
        entry.configure(state="normal")  # Entry'nin state'ini değiştir
        entry.delete(0, "end")
        entry.insert(0, selected_date)
        entry.configure(state="readonly")  # Entry'nin state'ini geri al
        top.destroy()

# Ana pencere oluştur
root = ctk.CTk()

# Tarih girişi için CTkDateEntry
tarih_entry = CTkDateEntry(root, width=12)
tarih_entry.pack(pady=10)

# Ana döngüyü başlat
root.mainloop()
