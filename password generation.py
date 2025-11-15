import customtkinter as ctk
from tkinter import messagebox
import random
import string
import math
import base64
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

NEON_BG = "#0b0f14"
PANEL_BG = "#0f1720"
NEON_ACCENT = "#00c2ff"
NEON_PINK = "#ff4dd2"
NEON_PURPLE = "#9b7bff"
SAVE_FILE = "passwords.txt"

root = ctk.CTk()
root.geometry("980x640")
root.title("Neon Cyber Password Studio")

main = ctk.CTkFrame(root, corner_radius=0, fg_color=NEON_BG)
main.pack(fill="both", expand=True)

sidebar = ctk.CTkFrame(main, width=200, corner_radius=0, fg_color="#0b0f12")
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(sidebar, text="⚡ CYBER", font=("Segoe UI", 20, "bold"), text_color=NEON_ACCENT)
logo.pack(pady=(18, 8))

def _sidebar_btn(master, text, cmd):
    btn = ctk.CTkButton(master, text=text, width=160, fg_color="#0f2140",
                       hover_color="#0b3a5a", command=cmd, corner_radius=12)
    return btn

content = ctk.CTkFrame(main, fg_color=NEON_BG)
content.pack(side="right", fill="both", expand=True, padx=18, pady=18)

pages = {}

def show_page(name):
    for p in pages.values():
        p.pack_forget()
    pages[name].pack(fill="both", expand=True)

gen_page = ctk.CTkFrame(content, fg_color=NEON_BG)
pages["gen"] = gen_page

title = ctk.CTkLabel(gen_page, text="⚙️  Password Generator", font=("Segoe UI", 26, "bold"), text_color=NEON_ACCENT)
title.pack(pady=(10, 6))

panel = ctk.CTkFrame(gen_page, width=680, height=360, corner_radius=14, fg_color=PANEL_BG)
panel.pack(pady=16)
panel.pack_propagate(False)

left_col = ctk.CTkFrame(panel, fg_color=PANEL_BG)
left_col.pack(side="left", padx=(24, 12), pady=18)

ctk.CTkLabel(left_col, text="Length", font=("Segoe UI", 14)).pack(anchor="w", pady=(6, 4))
length_entry = ctk.CTkEntry(left_col, width=140)
length_entry.pack(pady=(0, 8))
length_entry.insert(0, "14")

upper_var = ctk.BooleanVar(value=True)
lower_var = ctk.BooleanVar(value=True)
digits_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)

ctk.CTkCheckBox(left_col, text="Uppercase (A-Z)", variable=upper_var).pack(anchor="w", pady=4)
ctk.CTkCheckBox(left_col, text="Lowercase (a-z)", variable=lower_var).pack(anchor="w", pady=4)
ctk.CTkCheckBox(left_col, text="Digits (0-9)", variable=digits_var).pack(anchor="w", pady=4)
ctk.CTkCheckBox(left_col, text="Symbols (!@#$)", variable=symbols_var).pack(anchor="w", pady=4)

btn_frame = ctk.CTkFrame(left_col, fg_color=PANEL_BG)
btn_frame.pack(pady=(14,0))

def gen_action():
    try:
        length = int(length_entry.get())
    except:
        messagebox.showerror("Error", "Length must be a number")
        return
    chars = ""
    if upper_var.get(): chars += string.ascii_uppercase
    if lower_var.get(): chars += string.ascii_lowercase
    if digits_var.get(): chars += string.digits
    if symbols_var.get(): chars += string.punctuation
    if not chars:
        messagebox.showwarning("Select", "Choose at least one character type")
        return
    pwd = "".join(random.choice(chars) for _ in range(length))
    set_password(pwd, add_history=True)

def regenerate_action():
    if not result_entry.get():
        messagebox.showinfo("Info", "Generate first")
        return
    gen_action()

gen_btn = ctk.CTkButton(btn_frame, text="Generate", width=140, height=38, command=gen_action, fg_color=NEON_ACCENT)
gen_btn.grid(row=0, column=0, padx=6, pady=6)
regen_btn = ctk.CTkButton(btn_frame, text="Regenerate", width=140, height=38, command=regenerate_action, fg_color=NEON_PINK)
regen_btn.grid(row=0, column=1, padx=6, pady=6)

right_col = ctk.CTkFrame(panel, fg_color=PANEL_BG)
right_col.pack(side="left", padx=(12, 24), pady=18, fill="both", expand=True)

result_entry = ctk.CTkEntry(right_col, width=420, height=44, font=("Consolas", 16), justify="center")
result_entry.pack(pady=(12,8))

eye_btn_state = False
def toggle_eye():
    global eye_btn_state
    eye_btn_state = not eye_btn_state
    if eye_btn_state:
        result_entry.configure(show="")
        eye_btn.configure(text="🙈")
    else:
        result_entry.configure(show="*")
        eye_btn.configure(text="👁️")

eye_btn = ctk.CTkButton(right_col, text="👁️", width=50, command=toggle_eye)
eye_btn.pack(pady=(0, 8))

copy_btn = ctk.CTkButton(right_col, text="Copy", width=140, command=lambda: copy_password(False), fg_color=NEON_ACCENT)
copy_btn.pack(pady=(0,8))

strength_bar = ctk.CTkProgressBar(right_col, width=420)
strength_bar.set(0.0)
strength_bar.pack(pady=(6,6))

strength_label = ctk.CTkLabel(right_col, text="Entropy: 0 bits   •   Strength: —", font=("Segoe UI", 12))
strength_label.pack()

def save_to_file():
    pwd = result_entry.get()
    if not pwd:
        messagebox.showinfo("Info", "No password to save")
        return
    ts = datetime.now().isoformat(sep=" ", timespec="seconds")
    raw = f"{ts} :: {pwd}\n"
    encoded = base64.b64encode(raw.encode()).decode()
    with open(SAVE_FILE, "a", encoding="utf-8") as f:
        f.write(encoded + "\n")
    messagebox.showinfo("Saved", f"Password saved to {SAVE_FILE}")
    update_history_box(pwd)

save_btn = ctk.CTkButton(right_col, text="Save (Encrypted)", width=160, fg_color=NEON_PURPLE, command=save_to_file)
save_btn.pack(pady=(8,2))

hist_page = ctk.CTkFrame(content, fg_color=NEON_BG)
pages["hist"] = hist_page

h_title = ctk.CTkLabel(hist_page, text="📜 Stored & Session History", font=("Segoe UI", 24, "bold"), text_color=NEON_ACCENT)
h_title.pack(pady=12)

hist_panel = ctk.CTkFrame(hist_page, fg_color=PANEL_BG, corner_radius=12)
hist_panel.pack(padx=16, pady=8, fill="both", expand=True)

history_text = ctk.CTkTextbox(hist_panel, width=640, height=420, corner_radius=8)
history_text.pack(padx=16, pady=16)

def update_history_box(pwd):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_text.insert("0.0", f"{ts}  ::  {pwd}\n")

def load_saved_file():
    if not os.path.exists(SAVE_FILE):
        messagebox.showinfo("Info", "No saved file")
        return
    decoded = []
    with open(SAVE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if not line:
                continue
            try:
                decoded.append(base64.b64decode(line).decode())
            except:
                continue
    history_text.delete("0.0", "end")
    for entry in reversed(decoded):
        history_text.insert("0.0", entry)

load_btn = ctk.CTkButton(hist_page, text="Load Saved File", width=160, command=load_saved_file, fg_color=NEON_ACCENT)
load_btn.pack(pady=(6,0))

ai_page = ctk.CTkFrame(content, fg_color=NEON_BG)
pages["ai"] = ai_page

ai_title = ctk.CTkLabel(ai_page, text="🤖 AI Smart Passwords", font=("Segoe UI", 24, "bold"), text_color=NEON_PINK)
ai_title.pack(pady=12)

ai_panel = ctk.CTkFrame(ai_page, fg_color=PANEL_BG, corner_radius=12)
ai_panel.pack(padx=16, pady=8, fill="both", expand=True)

ai_entry = ctk.CTkEntry(ai_panel, width=560, height=44, font=("Consolas", 16), justify="center")
ai_entry.pack(pady=(24,12))

def ai_generate():
    adjs = ["Neon","Quantum","Silent","Crimson","Night","Iron","Nova","Phantom","Cyber","Solar","Shadow","Vortex"]
    nouns = ["Tiger","Falcon","Raptor","Ghost","Eagle","Knight","Viper","Phoenix","Nova","Drift","Specter"]
    sym = ["!", "@", "#", "$", "%", "&"]
    pwd = random.choice(adjs) + random.choice(nouns) + random.choice(sym) + str(random.randint(10,99))
    ai_entry.delete(0, "end")
    ai_entry.insert(0, pwd)
    set_password(pwd, add_history=True)

ai_btn = ctk.CTkButton(ai_panel, text="Generate AI Password", width=220, fg_color=NEON_PINK, command=ai_generate)
ai_btn.pack(pady=12)

ai_copy = ctk.CTkButton(ai_panel, text="Copy AI Password", width=200, command=lambda: copy_password(True), fg_color=NEON_ACCENT)
ai_copy.pack(pady=(8,12))

def entropy_estimate(password, use_upper, use_lower, use_digits, use_symbols):
    pool = 0
    if use_upper: pool += 26
    if use_lower: pool += 26
    if use_digits: pool += 10
    if use_symbols: pool += len(string.punctuation)
    if pool == 0:
        pool = len(set(password)) if password else 1
    bits = len(password) * math.log2(pool) if pool>0 else 0
    return round(bits, 1)

def set_password(pwd, add_history=False):
    result_entry.delete(0, "end")
    result_entry.insert(0, pwd)
    bits = entropy_estimate(pwd, upper_var.get(), lower_var.get(), digits_var.get(), symbols_var.get())
    val = max(0.0, min(bits / 100.0, 1.0))
    strength_bar.set(val)
    if bits < 28:
        strength_text = "Very Weak"
        color = "#ff3333"
    elif bits < 50:
        strength_text = "Weak"
        color = "#ff8c33"
    elif bits < 70:
        strength_text = "Good"
        color = "#ffd966"
    else:
        strength_text = "Strong"
        color = "#33ff99"
    strength_label.configure(text=f"Entropy: {bits} bits   •   Strength: {strength_text}", text_color=color)
    if add_history:
        update_history_box(pwd)

def copy_password(from_ai):
    pwd = ai_entry.get() if from_ai else result_entry.get()
    if not pwd:
        messagebox.showinfo("Info", "Nothing to copy")
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Copied", "Password copied to clipboard")

b1 = _sidebar_btn(sidebar, "Generator", lambda: show_page("gen"))
b1.pack(pady=(18,4))
b2 = _sidebar_btn(sidebar, "History", lambda: show_page("hist"))
b2.pack(pady=8)
b3 = _sidebar_btn(sidebar, "AI Studio", lambda: show_page("ai"))
b3.pack(pady=8)

credits = ctk.CTkLabel(sidebar, text="Neon v1.2", font=("Segoe UI", 10))
credits.pack(side="bottom", pady=12)


show_page("gen")
root.mainloop()
