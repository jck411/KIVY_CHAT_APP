# Android Development Quick Reference

## 🚨 **CRITICAL: Before Any Android Build**

```bash
# 1. Check Python Version (MUST be 3.10.x)
python --version  # Should show 3.10.x

# 2. If wrong version, switch to 3.10
uv python pin 3.10.12
uv sync

# 3. Install Android build tools
uv add --dev buildozer cython

# 4. Clean previous builds if changing dependencies
buildozer android clean
```

## 📱 **2025 Android Requirements**

| Requirement | Value | Notes |
|-------------|-------|-------|
| **Target API** | 35 | Mandatory for new apps Aug 31, 2025 |
| **Min API** | 21 | 99%+ device compatibility |
| **NDK** | r25b | Latest stable |
| **Python** | 3.10.x | **Critical**: 3.11+ breaks Buildozer |
| **Architectures** | arm64-v8a, armeabi-v7a | 64-bit + legacy support |

## 🔧 **Quick Build Commands**

```bash
# Debug build (for testing)
buildozer android debug

# Release build (for store)
buildozer android release

# Install on connected device
adb install bin/*.apk

# Debug logs
adb logcat -s "python:*" "kivy:*"
```

## ⚠️ **Common Build Failures**

| Error | Cause | Fix |
|-------|-------|-----|
| `'internal/pycore_frame.h' file not found` | Python 3.11+ | Use Python 3.10.x |
| `NDK not found` | Wrong NDK version | Update to NDK r25b |
| `Target API too low` | Old API target | Set `android.api = 35` |
| `Requirements not found` | Built-in modules listed | Remove asyncio, threading, json from requirements |

## 📊 **Performance Targets**

- **Startup time**: < 3 seconds
- **Memory usage**: < 150MB
- **APK size**: < 50MB (uncompressed)
- **UI responsiveness**: 60fps scrolling

## 🔒 **Production Checklist**

- [ ] Use WSS (not WS) for WebSocket connections
- [ ] Test on Android API 21, 28, 31, 35
- [ ] Generate release keystore
- [ ] Test on real devices (not just emulator)
- [ ] Enable ProGuard/R8 for release builds
- [ ] Test network connectivity edge cases
- [ ] Verify permissions are minimal and necessary 