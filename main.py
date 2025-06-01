import customtkinter
import tkinter as tk
import gelir_giderMenu
import gelir_ekleMenu
import gider_ekleMenu

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window

# Ekran genişliğini bulun
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()


# Ekran genişliğinin yarısını bulun
screen_width = screen_width * 0.8
screen_height = screen_height * 0.79


#app.geometry("400x240")
app.title("Gelir Gider Uygulaması")
#app.attributes('-fullscreen', True)
app.geometry("+0+0")
app.minsize(int(screen_width),int(screen_height))
#app.resizable(width = False, height = False) # Ekranı sabitlemek için

version = "v0.2.3"

#Label boyutları
label_width=250
label_height=25
label_corner_radius=3
label_font = ("Ariel", 15, "bold")
label_color = "#1ab394"


# Tab View
tabview = customtkinter.CTkTabview(master=app)
tabview.pack(side= tk.TOP,expand=True, fill="both")
gelir_gider = tabview.add("Analiz")  # add tab at the end
gelir_ekle = tabview.add("Gelir Ekle")  # add tab at the end
gider_ekle = tabview.add("Gider Ekle")

tabview.grid_propagate(False)


app.after(1, gelir_giderMenu.AllView(gelir_gider))
app.after(1, gelir_ekleMenu.AllView(gelir_ekle))
app.after(1, gider_ekleMenu.AllView(gider_ekle))



version_label = customtkinter.CTkLabel(app, text=f"Version: {version}", font=("Ariel", 12),fg_color="transparent")
version_label.place(relx=0.995, rely=0.999,anchor="se")


app.mainloop()