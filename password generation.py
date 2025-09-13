import tkinter as tk
from tkinter import messagebox
import random
import string

def generate_password():
    length = int(length_entry.get())
    include_upper = upper_var.get()
    include_lower = lower_var.get()
    include_digits = digits_var.get()
    include_symbols = symbols_var.get()

    chars = ""
    if include_upper:
        chars += string.ascii_uppercase
    if include_lower:
        chars += string.ascii_lowercase
    if include_digits:
        chars += string.digits
    if include_symbols:
        chars += string.punctuation

    if not chars:
        messagebox.showwarning("Error", "Select at least one character type")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    result_entry.delete(0, tk.END)
    result_entry.insert(0, password)

def copy_password():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard")

root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(frame, width=5)
length_entry.grid(row=0, column=1)
length_entry.insert(0, "12")

upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)

tk.Checkbutton(frame, text="Uppercase", variable=upper_var).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame, text="Lowercase", variable=lower_var).grid(row=2, column=0, sticky="w")
tk.Checkbutton(frame, text="Digits", variable=digits_var).grid(row=3, column=0, sticky="w")
tk.Checkbutton(frame, text="Symbols", variable=symbols_var).grid(row=4, column=0, sticky="w")

tk.Button(root, text="Generate", command=generate_password).pack(pady=5)
result_entry = tk.Entry(root, width=40, justify="center")
result_entry.pack(pady=5)
tk.Button(root, text="Copy", command=copy_password).pack(pady=5)

root.mainloop()
