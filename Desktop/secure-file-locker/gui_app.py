import tkinter as tk
from tkinter import filedialog, messagebox
import os
from engines.aes_engine import encrypt_file_aes, decrypt_file_aes
from engines.xor_engine import encrypt_file_xor, decrypt_file_xor
from utils.hasher import sha256_file
from utils.logger import log


# --------------------------
# Password Strength Checker
# --------------------------
def check_strength(password):
    length = len(password) >= 8
    upper = any(c.isupper() for c in password)
    lower = any(c.islower() for c in password)
    digit = any(c.isdigit() for c in password)
    special = any(not c.isalnum() for c in password)

    score = length + upper + lower + digit + special

    if score <= 2:
        return "Weak ❌"
    elif score == 3 or score == 4:
        return "Medium ⚠️"
    else:
        return "Strong ✅"


# --------------------------
# Live Password Window
# --------------------------
def get_password_window():
    win = tk.Toplevel()
    win.title("Enter Password")
    win.geometry("350x160")
    win.resizable(False, False)

    tk.Label(win, text="Enter Password:", font=("Arial", 12)).pack(pady=5)

    password_var = tk.StringVar()
    entry = tk.Entry(win, textvariable=password_var, show="*", width=30, font=("Arial", 12))
    entry.pack(pady=5)

    strength_label = tk.Label(win, text="Strength: ", font=("Arial", 11))
    strength_label.pack()

    # Update strength live
    def on_type(*args):
        pwd = password_var.get()
        if pwd:
            strength_label.config(text=f"Strength: {check_strength(pwd)}")
        else:
            strength_label.config(text="Strength: ")

    password_var.trace("w", on_type)

    password_value = {"pwd": None}

    def submit():
        password_value["pwd"] = password_var.get()
        win.destroy()

    tk.Button(win, text="OK", width=10, command=submit).pack(pady=10)

    entry.focus()
    win.wait_window()
    return password_value["pwd"]


# --------------------------
# Auto rename if file exists
# --------------------------
def auto_rename(path):
    if not os.path.exists(path):
        return path
    base, ext = os.path.splitext(path)
    counter = 1
    new_path = f"{base}({counter}){ext}"
    while os.path.exists(new_path):
        counter += 1
        new_path = f"{base}({counter}){ext}"
    return new_path


# --------------------------
# GUI Class
# --------------------------
class SecureLockerGUI:
    def __init__(self, root):
        self.root = root
        root.title("🔐 Secure File Locker")
        root.geometry("420x360")
        root.resizable(False, False)

        tk.Label(root, text="Secure File Locker", font=("Arial", 18, "bold")).pack(pady=12)

        tk.Button(root, text="Encrypt (AES)", width=25, command=self.encrypt_aes).pack(pady=4)
        tk.Button(root, text="Decrypt (AES)", width=25, command=self.decrypt_aes).pack(pady=4)
        tk.Button(root, text="Encrypt (XOR)", width=25, command=self.encrypt_xor).pack(pady=4)
        tk.Button(root, text="Decrypt (XOR)", width=25, command=self.decrypt_xor).pack(pady=4)
        tk.Button(root, text="Check File Hash (SHA256)", width=25, command=self.check_hash).pack(pady=4)
        tk.Button(root, text="Exit", width=25, command=root.quit).pack(pady=12)

    def choose_file(self):
        return filedialog.askopenfilename()

    # --------------------------
    # AES Encryption
    # --------------------------
    def encrypt_aes(self):
        inp = self.choose_file()
        if not inp: return

        password = get_password_window()
        if not password: return

        directory, fname = os.path.split(inp)
        name, ext = os.path.splitext(fname)

        out = os.path.join(directory, f"{name}_encrypted{ext}.aes")
        out = auto_rename(out)

        encrypt_file_aes(inp, out, password)

        messagebox.showinfo("Done", f"AES Encryption Completed!\nSaved to:\n{out}")
        log(f"AES encrypted: {inp} → {out}")

    # --------------------------
    # AES Decryption (restore original extension)
    # --------------------------
    def decrypt_aes(self):
        inp = self.choose_file()
        if not inp: return

        password = get_password_window()
        if not password: return

        directory, fname = os.path.split(inp)

        # original extension (remove "_encrypted")
        original_name = fname.replace("_encrypted", "").replace(".aes", "")

        # restore extension automatically
        out = os.path.join(directory, original_name)
        out = auto_rename(out)

        status = decrypt_file_aes(inp, out, password)

        if status:
            messagebox.showinfo("Done", f"AES Decryption Completed!\nSaved to:\n{out}")
            log(f"AES decrypted: {inp} → {out}")
        else:
            messagebox.showerror("Error", "Wrong password or corrupted file")
            log("AES decrypt failed")

    # --------------------------
    # XOR Encryption
    # --------------------------
    def encrypt_xor(self):
        inp = self.choose_file()
        if not inp: return

        key = get_password_window()
        if not key: return

        directory, fname = os.path.split(inp)
        name, ext = os.path.splitext(fname)

        out = os.path.join(directory, f"{name}_xor{ext}.enc")
        out = auto_rename(out)

        encrypt_file_xor(inp, out, key)

        messagebox.showinfo("Done", f"XOR Encryption Completed!\nSaved to:\n{out}")
        log(f"XOR encrypted: {inp} → {out}")

    # --------------------------
    # XOR Decryption (restore original extension)
    # --------------------------
    def decrypt_xor(self):
        inp = self.choose_file()
        if not inp: return

        key = get_password_window()
        if not key: return

        directory, fname = os.path.split(inp)

        original_name = fname.replace("_xor", "").replace(".enc", "")
        out = os.path.join(directory, original_name)
        out = auto_rename(out)

        decrypt_file_xor(inp, out, key)

        messagebox.showinfo("Done", f"XOR Decryption Completed!\nSaved to:\n{out}")
        log(f"XOR decrypted: {inp} → {out}")

    # --------------------------
    # Hash
    # --------------------------
    def check_hash(self):
        inp = self.choose_file()
        if not inp: return

        file_hash = sha256_file(inp)
        messagebox.showinfo("SHA256", f"Hash:\n{file_hash}")
        log(f"Hash checked: {inp}")
