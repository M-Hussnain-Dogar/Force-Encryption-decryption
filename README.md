"""
Windows Folder File Encryptor/Decryptor with GUI Summary

Description:
This script performs recursive encryption or decryption of all files within a specified folder using AES-256 encryption in CBC mode. It includes:

- Administrator privilege escalation
- Ownership and permission manipulation (via `takeown`, `icacls`, `attrib`)
- Secure key handling (manual or auto-generated 256-bit key)
- Identification of previously encrypted files using a custom "ENC!" header
- Use of multithreading for efficient file processing
- Interactive Tkinter GUI to summarize success/failure, display encryption key, and show background image

Key Features:
- Safe handling of already-encrypted or corrupted files
- Full control over Windows Explorer processes to avoid file locking issues
- Displays key warnings and logs in an elegant full-screen interface
- AES encryption includes IV and custom padding

Dependencies:
- `pycryptodome`, `Pillow`, `tkinter`, `psutil`

Warning:
🔐 Always store the encryption key securely. Without it, decryption is impossible.

"""
