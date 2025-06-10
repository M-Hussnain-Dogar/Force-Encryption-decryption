import subprocess
import os
import time
import keyboard

# Set ADB path (wrapped in quotes to handle spaces)
ADB_PATH = r'"D:\apps---\mobile tools\platform-tools-latest-windows\platform-tools\adb.exe"'
IP_FILE = "last_ip.txt"  # File to store the last used IP address

def send_command(command):
    """Runs an ADB command and returns the output."""
    try:
        result = subprocess.run(f"{ADB_PATH} {command}", shell=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("❌ Error executing command!")
        return None

def is_device_connected():
    """Check if a device is connected via ADB."""
    output = send_command("devices")
    return "device" in output if output else False

def is_phone_locked():
    """Check if the phone is locked using a faster method."""
    output = send_command("shell dumpsys deviceidle get screen")  # Gets screen state
    
    if "off" in output.lower():
        return True  # Phone is locked
    
    output = send_command("shell dumpsys window policy")  # Check keyguard status
    return "showing=true" in output

def unlock_phone():
    """Prompt user to enter phone password until it's unlocked."""
    if not is_phone_locked():
        print("✅ Phone is already unlocked!")
        return

    while is_phone_locked():
        password = input("🔓 Enter phone's password/PIN to unlock: ").strip()
        if password:
            send_command("shell input swipe 500 1080 500 600")
            send_command(f"shell input text {password}")
            send_command("shell input keyevent 66")  # Press Enter key
            time.sleep(2)  # Give time to check if phone unlocks
            if not is_phone_locked():
                print("✅ Phone unlocked successfully!")
                break
            else:
                print("Incorrect password")

def connect_via_wifi(ip):
    """Connect to the phone via WiFi ADB."""
    print(f"🔄 Restarting ADB in TCP/IP mode...")
    send_command("tcpip 5555")
    time.sleep(2)  # Wait for the command to take effect
    
    print(f"🔄 Connecting to {ip}:5555...")
    send_command(f"connect {ip}:5555")
    time.sleep(2)  # Wait for the connection attempt

def get_last_ip():
    """Retrieve the last used IP from file."""
    if os.path.exists(IP_FILE):
        with open(IP_FILE, "r") as file:
            return file.read().strip()
    return None

def save_ip(ip):
    """Save the IP for future use."""
    with open(IP_FILE, "w") as file:
        file.write(f"{ip}")
def stop():
    if keyboard.is_pressed("ctrl+A") or keyboard.is_pressed("ctrl+a") or keyboard.is_pressed("esc"):
       exit
def update_adb_ip():
    """Prompt user to enter a new IP and update ADB connection."""
    last_ip = get_last_ip()
    if last_ip:
        print(f"ℹ️   Last used IP: {last_ip}")
    
    ip = input("Enter phone's IP address (or press Enter to use last IP): ").strip()
    if not ip and last_ip:
        ip = last_ip

    if ip:
        save_ip(ip)
        connect_via_wifi(ip)

    if is_device_connected():
        print("✅ Device connected successfully!")
    else:
        print("❌ Device still not detected! Make sure USB Debugging & Wireless Debugging are enabled.")

def control_phone():
    """Menu to control the phone via ADB."""
    if not is_device_connected():
        print("❌ No device detected! Trying to reconnect via WiFi...")
        update_adb_ip()
        if not is_device_connected():
            print("❌ Connection failed. Exiting...")
            return
    while True:
        print("\n🔹 Mobile Control Menu 🔹")
        print("1. Tap on screen")
        print("2. Swipe gesture")
        print("3. Press a button (Home, Back, etc.)")
        print("4. Launch an app")
        print("5. Type text")
        print("6. Take a screenshot")
        print("7. Get device info")
        print("8. Reboot phone")
        print("9. Enable/Disable Wi-Fi")
        print("10. Enable/Disable Airplane Mode")
        print("11. Rotate screen")
        print("12. Adjust volume")
        print("13. Change IP & Reconnect")
        print("14. Unlock Phone (if locked)")
        print("\n🔹loops🔹")
        print("15. Press a button loop(Home, Back, etc.)")
        print("16. Launch an app loop")
        print("17. Enable/Disable Wi-Fi")
        print("18. Enable/Disable Airplane Mode")
        print("19. Adjust volume")
        print("20. Exit")
        print("[Note] Press ctrl and A or ctrl and a at same time or press esc to stop loop.")
        choice = input("Enter your choice: ")

        if choice == "1":
            x, y = input("Enter X and Y coordinates (e.g., 500 500): ").split()
            send_command(f"shell input tap {x} {y}")
        elif choice == "2":
            x1, y1, x2, y2 = input("Enter start (X1, Y1) and end (X2, Y2) coordinates: ").split()
            send_command(f"shell input swipe {x1} {y1} {x2} {y2}")
        elif choice == "3":
            abc = True
            while abc == True:
             print("Keys: \n---Navigation Keys---\n 3.home\n 4.back\n 5.call\n 6.end call\n 82.menu\n 187.recent apps\n---Volume and powerkeys---\n 24.Volume up\n 25.volume down\n 26.power\n 164.mute\n---media controls---\n 85.play/pause\n 86.stop\n 87.Next\n 88.Back\n 90.fast\n 91.close media\n---Directional keys---\n 19.UP\n 20.Down\n 21.left\n 22.right\n 23.center\n---Meta/system---\n 157.left meta\n 158.rightmeta\n 175.Brighteness down\n 176.Brightness up\n 183.Google Assistant\n---Camera controls---\n 27.Camer\n 80.Focus\n 81.zoom in\n 82.zoom out\n---Others---\n 170.Voice input\n 66.Enter\n a.exit")
             key = input("Enter key code: ")
             if(key!="a"):
              send_command(f"shell input keyevent {key}")
             if key == "a":
                 abc = False
        elif choice == "4":
            package = input("Enter app package name (e.g., com.android.chrome): ")
            send_command(f"shell monkey -p {package} -c android.intent.category.LAUNCHER 1")
        elif choice == "5":
            text = input("Enter text to type: ")
            send_command(f"shell input text \"{text}\"")
        elif choice == "6":
            send_command("shell screencap -p /sdcard/screenshot.png")
            send_command("pull /sdcard/screenshot.png screenshot.png")
            print("✅ Screenshot saved as 'screenshot.png'")
        elif choice == "7":
            send_command("shell getprop ro.product.model")
            send_command("shell dumpsys battery | grep level")
        elif choice == "8":
            send_command("reboot")
        elif choice == "9":
            action = input("Enter 'on' to enable Wi-Fi or 'off' to disable: ")
            send_command("shell svc wifi enable" if action == "on" else "shell svc wifi disable")
        elif choice == "10":
            action = input("Enter 'on' to enable Airplane Mode or 'off' to disable: ")
            send_command("shell settings put global airplane_mode_on 1") if action == "on" else send_command("shell settings put global airplane_mode_on 0")
            send_command(f"shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state {'true' if action == 'on' else 'false'}")
        elif choice == "11":
            rotation = input("Enter rotation (0=Portrait, 1=Landscape Right, 2=Upside Down, 3=Landscape Left): ")
            send_command(f"shell settings put system user_rotation {rotation}")
        elif choice == "12":
            action = input("Enter 'up', 'down', or 'mute': ")
            keycode = {"up": "24", "down": "25", "mute": "164"}.get(action, "")
            if keycode:
                send_command(f"shell input keyevent {keycode}")
        elif choice == "13":
            update_adb_ip()
        elif choice == "14":
            unlock_phone()  # Unlock phone if locked
        elif choice == "15":
            print("Key codes: 3=Home, 4=Back, 24=Vol Up, 25=Vol Down, 26=Power")
            key = input("Enter key code: ")
            loop1 = input("Enter loop number: ")
            for i in range(int(loop1)):
             stop()
             time.sleep(0.5)
             send_command(f"shell input keyevent {key}")
        elif choice == "16":
            package = input("Enter app package name (e.g., com.android.chrome): ")
            loop1 = input("Enter loop number: ")
            for i in range(int(loop1)):
              stop()
              time.sleep(0.5)
              send_command(f"shell monkey -p {package} -c android.intent.category.LAUNCHER 1")
        elif choice == "17":
            action = input("Enter 'on' to enable Wi-Fi or 'off' to disable: ")
            loop1 = input("Enter loop number: ")
            for i in range(int(loop1)):
              stop()
              time.sleep(0.5)
              send_command("shell svc wifi enable" if action == "on" else "shell svc wifi disable")
        elif choice == "18":
            action = input("Enter 'on' to enable Airplane Mode or 'off' to disable: ")
            loop1 = input("Enter loop number: ")
            for i in range(int(loop1)):
              stop()
              time.sleep(0.5)
              send_command("shell settings put global airplane_mode_on 1") if action == "on" else send_command("shell settings put global airplane_mode_on 0")
              send_command(f"shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state {'true' if action == 'on' else 'false'}")
        elif choice == "19":
            action = input("Enter 'up', 'down', or 'mute': ")
            keycode = {"up": "24", "down": "25", "mute": "164"}.get(action, "")
            if keycode:
                 loop1 = input("Enter loop number: ")
                 for i in range(int(loop1)):
                  stop()
                  time.sleep(0.5)
                  send_command(f"shell input keyevent {keycode}")
        elif choice == "20":
            print("Exiting...")
            break
        else:
            print("❌ Invalid choice, try again.")

def main():
    """Main function to check connection and start phone control."""
    update_adb_ip()  # Ask for IP first before checking connection
    control_phone()

if __name__ == "__main__":
    main()
