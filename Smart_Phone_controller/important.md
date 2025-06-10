# Important: Using `adb devices`

## Requirements

1. **Install ADB (Android Debug Bridge)**
   - Download the Android SDK Platform-Tools from:
     [https://developer.android.com/studio/releases/platform-tools](https://developer.android.com/studio/releases/platform-tools)

2. **Enable Developer Options on Android Device**
   - Go to `Settings > About phone`
   - Tap **Build number** 7 times to unlock Developer Options

3. **Enable USB Debugging**
   - Go to `Settings > Developer options`
   - Turn on **USB Debugging**

4. **Connect Device via USB**
   - Use a reliable USB cable
   - Confirm "Allow USB debugging" prompt on the phone if it appears

5. **Install USB Drivers (Windows only)**
   - Install OEM-specific drivers from the device manufacturer

6. **Verify Device Connection**
   ```sh
   adb devices
