def on_focus_in(event):
    if gelirTutariEntry.get() == "Enter tutar":
        gelirTutariEntry.delete(0, "end")
        gelirTutariEntry.configure(fg_color="black")

def on_focus_out(event):
    if not gelirTutariEntry.get():
        gelirTutariEntry.insert(0, "Enter tutar")
        gelirTutariEntry.configure(fg_color="grey")


gelirTutariEntry = customtkinter.CTkEntry(new_window,placeholder_text="Gelir Tutarı",validate="key",validatecommand=(new_window.register(validate_tutar), '%S'),  width = entryWidth)
gelirTutariEntry.insert(0, "Enter tutar")
gelirTutariEntry.configure(fg_color="grey")
gelirTutariEntry.bind("<FocusIn>", on_focus_in)
gelirTutariEntry.bind("<FocusOut>", on_focus_out)