# 📱 Android Deployment Guide

This guide walks you through deploying your KivyMD Chat App to Android using Buildozer.

## 📅 **Current Requirements (January 2025)**

**Google Play Store requires:**
- **Target API 35** for new apps (mandatory from August 31, 2025)
- **Minimum API 21** for broad device compatibility
- **NDK r25b** (latest stable)
- **Python 3.9-3.11** (Buildozer has compatibility issues with 3.12+)

## 🛠️ Prerequisites

### **System Requirements**
- Linux or macOS (WSL2 for Windows)
- **Python 3.9-3.11** (Android builds have issues with 3.12+, avoid 3.13+)
- Java JDK 17 (JDK 11 also works but 17 is recommended)
- At least 8GB RAM and 50GB free disk space

### **Install Dependencies**

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

**macOS:**
```bash
brew install python3 openjdk@17 autoconf automake libtool pkg-config
export JAVA_HOME=$(/usr/libexec/java_home -v17)
```

### **Install Buildozer**
```bash
pip3 install --upgrade buildozer
pip3 install --upgrade cython
```

## 🚀 Building for Android

### **1. Prepare Your Environment**
```bash
# Navigate to your project directory
cd /path/to/KIVY_CHAT_APP

# Verify buildozer.spec exists
ls buildozer.spec

# Initialize buildozer (first time only)
buildozer android debug
```

### **2. Configure Build Settings**
Edit `buildozer.spec` if needed:

```ini
# For release builds, you might want to adjust:
[app]
title = Your Chat App Name
package.name = yourchatapp
package.domain = com.yourcompany

# Add any custom requirements
requirements = python3,kivy==2.3.1,kivymd==1.2.0,websockets==13.1,requests

# Set orientation (portrait recommended for chat)
orientation = portrait
```

### **3. Build Debug APK**
```bash
# Clean build (recommended for first build)
buildozer android clean

# Build debug APK
buildozer android debug

# APK will be in: bin/kivychat-0.1.0-arm64-v8a_armeabi-v7a-debug.apk
```

### **4. Build Release APK**
```bash
# Generate a keystore (first time only)
keytool -genkey -v -keystore my-release-key.keystore -alias alias_name -keyalg RSA -keysize 2048 -validity 10000

# Build release APK
buildozer android release

# Sign the APK (buildozer will prompt for keystore password)
```

## 📱 Testing on Device

### **Install Debug APK**
```bash
# Enable Developer Options and USB Debugging on your Android device
# Connect device via USB

# Install via ADB
adb install bin/kivychat-0.1.0-arm64-v8a_armeabi-v7a-debug.apk

# Or install manually by copying APK to device
```

### **Monitor Logs**
```bash
# View app logs in real-time
adb logcat | grep python

# Or view specific app logs
adb logcat -s "python:*"
```

## 🐛 Common Build Issues

### **1. Build Fails with "NDK not found"**
```bash
# Buildozer will auto-download, but if it fails:
buildozer android update
```

### **2. "Permission denied" or "Command not found"**
```bash
# Ensure buildozer is in PATH
export PATH=$PATH:~/.local/bin

# Make buildozer executable
chmod +x ~/.local/bin/buildozer
```

### **3. Memory Issues During Build**
```bash
# Increase Java heap size
export GRADLE_OPTS="-Xmx4g -Dorg.gradle.parallel=false"
```

### **4. WebSocket Connection Issues on Android**
- Ensure your backend server is accessible from the device's network
- Use IP address instead of 'localhost' in WebSocket URI
- Add network security config if connecting to HTTP endpoints

### **5. App Crashes on Startup**
```bash
# Check logs for Python errors
adb logcat -s "python:*" "kivy:*"

# Common fixes:
# - Verify all dependencies are in requirements
# - Check for unsupported Python 3.12+ features
# - Ensure no desktop-specific code is running on mobile
```

### **6. Python Version Compatibility Issues**
```bash
# If you get errors related to 'internal/pycore_frame.h' or similar:
# This indicates Python 3.11+ compatibility issues with Buildozer

# Solution: Use Python 3.9 or 3.10 for building
pyenv install 3.10.12
pyenv local 3.10.12

# Or use a virtual environment with correct Python version
python3.10 -m venv android_build_env
source android_build_env/bin/activate
```

## 📦 App Store Deployment

### **1. Prepare Release Build**
```bash
# Build signed release APK
buildozer android release

# Or build AAB for Google Play Store
buildozer android aab
```

### **2. Google Play Store Requirements**
- **Target API level 35** (required for new apps starting August 31, 2025)
- **Minimum API level 21** for maximum device compatibility
- 64-bit support (arm64-v8a included)
- Signed with upload key
- Privacy policy if app collects data
- App bundle format (AAB) preferred

### **3. Upload to Play Console**
1. Create developer account at https://play.google.com/console
2. Create new application
3. Upload AAB/APK file
4. Fill in store listing details
5. Set content rating and pricing
6. Submit for review

## 🔧 Optimizations

### **Mobile-Specific Features**
The app automatically detects Android and applies:
- Touch-friendly UI sizing
- Mobile-optimized WebSocket settings
- Proper keyboard handling
- Network-aware connection management

### **Performance Tips**
- Test on various Android versions (API 21+)
- Monitor memory usage with Android profiler
- Optimize image assets for different screen densities
- Test network connectivity scenarios

### **Security Considerations**
- Use HTTPS/WSS for production WebSocket connections
- Implement certificate pinning for sensitive data
- Add network security configuration for cleartext traffic
- Consider app signing key security

## 📋 Build Checklist

Before releasing:
- [ ] Test on multiple Android devices/versions
- [ ] Verify WebSocket connections work on mobile networks
- [ ] Check app permissions are minimal and necessary
- [ ] Test offline/demo mode functionality
- [ ] Verify UI scaling on different screen sizes
- [ ] Test keyboard interactions and text input
- [ ] Ensure app handles Android lifecycle properly
- [ ] Check memory usage and performance
- [ ] Test app update scenarios
- [ ] Verify crash reporting works

## 🆘 Getting Help

**Buildozer Issues:**
- Buildozer documentation: https://buildozer.readthedocs.io/
- Kivy Discord: https://chat.kivy.org/

**KivyMD Issues:**
- KivyMD documentation: https://kivymd.readthedocs.io/
- GitHub issues: https://github.com/kivymd/KivyMD/issues

**Android Specific:**
- Check `buildozer.spec` configuration
- Review Android logs via `adb logcat`
- Test with different Android API levels 