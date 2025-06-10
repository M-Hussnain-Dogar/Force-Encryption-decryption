"""
ADB Android Phone Control Tool
Author: [Your Name]
Date: [Optional]

Description:
This script enables remote control of an Android device via ADB (Android Debug Bridge). It supports connection over USB or Wi-Fi (via IP address) and offers an interactive terminal menu for the following features:

Key Features:
- Connect to a phone over USB or Wi-Fi ADB (TCP/IP)
- Auto-detect if the phone is locked and allow manual unlocking
- Send screen taps, swipes, key events (e.g., volume, power, home)
- Launch applications by package name
- Enter custom text
- Take screenshots and retrieve them to the PC
- Enable/disable system settings (Wi-Fi, Airplane Mode)
- Rotate screen and control volume
- Run actions in loops (e.g., repeated taps or key events)
- Save and reuse IP addresses for faster reconnection

Requirements:
- ADB installed and path correctly set in the script
- Python 3.6+
- `keyboard` module (`pip install keyboard`)

Note:
- The script supports soft loops and custom key combinations (like Ctrl+A or Esc) to break loops.
- Ideal for automation, testing, or remote interaction with an Android device.

"""
