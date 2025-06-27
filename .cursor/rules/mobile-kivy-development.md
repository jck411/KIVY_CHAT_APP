# Mobile Kivy Development Rules

## **Python Version & Environment Management**
- **Pin Python 3.10.x** for Android compatibility (`python = "==3.10.12"`); Buildozer has critical issues with 3.11+ including 'internal/pycore_frame.h' errors
- Use **separate environments** for desktop (`3.13.x`) vs Android builds (`3.10.x`): `uv python pin 3.10.12` in project root for Android compatibility
- **Never** use Python 3.12+ for Android builds—known incompatibilities with python-for-android/Buildozer toolchain
- Update monthly: `uv python install 3.10.13 && uv sync` but stay within 3.10.x range for Android projects
- Create dedicated build environments: `uv venv android-build --python 3.10.12` for Android compilation

## **UV Package Management & Execution**
- Use **uv exclusively** for all Python operations: `uv add/remove/sync` for dependencies, `uv run` for execution, `uv venv` for environments; **never** use pip, pipx, poetry, conda, or python -m
- Execute scripts via `uv run module:main` or `uv run script.py`—avoid `python -m module` or direct python execution that bypasses uv's resolver
- Manage dependencies in `pyproject.toml` with caret ranges (`^1.2.3`); use `uv add --dev` for development dependencies and `uv sync` for lockfile updates
- **For Android projects**: Constrain Python version `requires-python = ">=3.10.0,<3.11"` to prevent Buildozer incompatibilities
- **Never** create requirements.txt files or use `pip install -r`—uv handles everything through pyproject.toml and uv.lock for reproducible builds

## **Android Build Configuration**
- **Target API 35** minimum (required for Google Play Store new apps from August 31, 2025)
- **Minimum API 21** for maximum device compatibility (covers 99%+ of active Android devices)
- **NDK r25b** (latest stable)—avoid older versions that lack ARM64 optimizations
- Use **buildozer.spec** with proper architecture targeting: `android.archs = arm64-v8a, armeabi-v7a`
- **Never** include built-in Python modules in requirements (asyncio, threading, json, time)—only third-party packages
- Configure appropriate **permissions**: `INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK` (minimal set for chat apps)

## **Mobile-Responsive UI Design**
- Implement **platform detection** (`from kivy.utils import platform`) to adapt UI for mobile vs desktop
- Use **touch-friendly sizing**: minimum 44dp touch targets (Material Design), larger spacing on mobile (`dp(16)` vs `dp(12)`)
- **Responsive layouts**: Never set fixed window sizes on mobile—use `size_hint` and `adaptive_height/width`
- **Keyboard handling**: Configure `keyboard_mode = 'systemandmulti'` for proper Android keyboard integration
- **ScrollView optimization**: Implement scroll throttling (`100ms`) to maintain 60fps during rapid updates

## **WebSocket Streaming & Real-time Communication**
- Maintain **persistent WebSocket connections** with dedicated background threads; never create new connections per message or operation
- Process streaming chunks **immediately upon arrival**—eliminate all artificial batching delays, buffering, or scheduled processing that adds latency
- Use direct UI updates via thread-safe mechanisms (Kivy Clock.schedule_once); avoid complex batching systems that cause race conditions
- Configure connections with compression (`deflate`), **mobile-optimized timeouts** (`ping_interval: 30s` for mobile vs `120s` desktop), and exponential backoff reconnection logic
- **Mobile network adaptation**: Shorter timeouts (`15s` connection), more retries (`5` vs `3`), adaptive retry delays for unstable mobile connections
- **Never** add artificial delays to "smooth" streaming—modern frameworks handle real-time updates efficiently when unbuffered

## **Performance & Memory Management**
- Implement **message history limits** (`MAX_MESSAGE_HISTORY = 100`) to prevent memory leaks on mobile devices
- Use **lazy loading** and **cleanup strategies**: Remove old UI widgets when scrolling exceeds thresholds
- **Battery optimization**: Implement proper app lifecycle handling—pause WebSocket on background, resume on foreground
- **Connection state management**: Implement `ConnectionState` enum with proper state transitions and user feedback
- **Demo mode fallback**: Always provide offline functionality when backend unavailable

## **Development Workflow**
- **Test on real Android devices** early and often—emulators don't accurately reflect performance/network conditions
- Use **adb logcat** for debugging: `adb logcat -s "python:*" "kivy:*"` to filter relevant logs
- **Clean builds** frequently: `buildozer android clean` when changing dependencies or configuration
- **Version control**: `.gitignore` buildozer build artifacts (`.buildozer/`, `bin/`) but commit `buildozer.spec`
- **Staged deployment**: Debug APK → Internal testing → Alpha → Beta → Production release

## **Security & Production Readiness**
- Use **HTTPS/WSS** for all production WebSocket connections—never cleartext in production
- Implement **certificate pinning** for sensitive data transmission
- **Environment configuration**: Use `os.getenv()` for all configurable values—never hardcode endpoints
- **Error handling**: Graceful degradation with user-friendly error messages, avoid exposing technical details
- **App signing**: Generate proper keystores for release builds, secure key management for Play Store uploads

## **Cross-Platform Considerations**
- **Conditional imports**: Use try/except for platform-specific modules to avoid import errors
- **File paths**: Use `os.path.join()` and avoid hardcoded separators for cross-platform compatibility
- **Network configuration**: Different WebSocket settings for mobile vs desktop (timeouts, retries, ping intervals)
- **Resource optimization**: Compress images for mobile, use appropriate DPI scaling for different screen densities
- **Testing matrix**: Test on Android API 21, 28, 31, 35 minimum for compatibility verification

## **Build System Best Practices**
- **Separate build environments**: Desktop development with latest Python, Android builds with 3.10.x
- **Dependency pinning**: Use exact versions in `buildozer.spec` requirements for reproducible Android builds
- **CI/CD considerations**: Use Docker containers with proper Android SDK/NDK setup for consistent builds
- **Build caching**: Configure buildozer to reuse distributions (`--dist_name`) to speed up iterative builds
- **Release automation**: Script the complete build → sign → upload pipeline for consistent releases 