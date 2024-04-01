import tkinter as tk
from tkinter import filedialog, Menu, Text, INSERT, END, WORD, messagebox, simpledialog, colorchooser, ttk
import re

def new_file():
    entry.delete(1.0, END)
    update_status("New File Created")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[('Text file', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            entry.delete(1.0, END)
            entry.insert(INSERT, content)
        update_status(f"Opened: {file_path}")

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text file', '*.txt')])
    if file_path:
        with open(file_path, 'w') as file:
            text = entry.get(1.0, END)
            file.write(text)
        update_status(f"Saved: {file_path}")

def cut_text():
    selected_text = entry.get(tk.SEL_FIRST, tk.SEL_LAST)
    try:
        parent.clipboard_clear()
        parent.clipboard_append(selected_text)
    except tk.TclError:
        messagebox.showerror("Error", "Failed to copy text to clipboard.")
    entry.delete(tk.SEL_FIRST, tk.SEL_LAST)
    update_status("Text Cut to Clipboard")

def copy_text():
    selected_text = entry.get(tk.SEL_FIRST, tk.SEL_LAST)
    try:
        parent.clipboard_clear()
        parent.clipboard_append(selected_text)
    except tk.TclError:
        messagebox.showerror("Error", "Failed to copy text to clipboard.")
    update_status("Text Copied to Clipboard")

def paste_text():
    try:
        text_to_paste = parent.clipboard_get()
        entry.insert(tk.SEL_FIRST, text_to_paste)
    except tk.TclError:
        messagebox.showerror("Error", "Failed to paste text from clipboard.")
    update_status("Text Pasted from Clipboard")

def change_font():
    font_str = simpledialog.askstring("Font Chooser", "Enter font specifications (e.g., Arial 12 bold):")
    try:
        custom_font = tk.Font(font=font_str)
        entry.config(font=custom_font)
        update_status(f"Font Changed: {font_str}")
    except tk.TclError:
        messagebox.showerror("Error", "Invalid font specifications. Please try again.")

def change_text_color():
    color = colorchooser.askcolor(title="Choose Text Color")[1]
    if color:
        entry.tag_configure("text_color", foreground=color)
        entry.config(foreground=color) 
        update_status(f"Text Color Changed: {color}")

def find_text():
    find_str = simpledialog.askstring("Find", "Enter text to find:")
    if find_str:
        start_pos = entry.search(find_str, 1.0, END)
        if start_pos:
            end_pos = f"{start_pos}+{len(find_str)}c"
            entry.tag_remove(tk.SEL, 1.0, END)
            entry.tag_add(tk.SEL, start_pos, end_pos)
            entry.mark_set(tk.INSERT, start_pos)
            entry.see(tk.INSERT)

def replace_text():
    find_str = simpledialog.askstring("Find", "Enter text to find:")
    if find_str:
        replace_str = simpledialog.askstring("Replace", "Enter text to replace:")
        if replace_str:
            start_pos = entry.search(find_str, 1.0, END)
            while start_pos:
                end_pos = f"{start_pos}+{len(find_str)}c"
                entry.delete(start_pos, end_pos)
                entry.insert(start_pos, replace_str)
                start_pos = entry.search(find_str, end_pos, END)

def about():
    messagebox.showinfo("About SwiftText", "SwiftText - A Simple Text Editor\nVersion 1.0\nDeveloped by - Parivesh, Shalini, Vighensh")



def update_status(message):
    status_var.set(message)
    parent.after(3000, clear_status)

def clear_status():
    status_var.set("Ready")

def auto_save():
    save_file()
    parent.after(60000, auto_save)  # Auto-save every 60 seconds (adjust as needed)

def change_theme():
    theme_color = colorchooser.askcolor(title="Choose Background Color")[1]
    if theme_color:
        entry.config(bg=theme_color)
        update_status(f"Theme Changed: {theme_color}")

parent = tk.Tk()
parent.title("swifttext")
parent.geometry("600x400")
parent.config(bg="LightBlue1")

menu_bar = Menu(parent)
parent.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=parent.quit)

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_separator()
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)

format_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Format", menu=format_menu)
format_menu.add_command(label="Change Font", command=change_font)
format_menu.add_command(label="Change Text Color", command=change_text_color)
format_menu.add_command(label="Change Theme", command=change_theme)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about ,foreground="red")

status_var = tk.StringVar()
status_bar = tk.Label(parent, textvariable=status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

sc = ttk.Scrollbar(parent, orient='vertical')
entry = Text(parent, height=100, width=180, wrap=WORD)
sc.pack(side=tk.RIGHT, fill='y')
sc.config(command=entry.yview)
entry.pack(pady=10, padx=10)

update_status("Ready")
parent.after(60000, auto_save)  # Start auto-save after 60 seconds

parent.mainloop()