# 📱 KivyMD Chat App - Project Development Plan

This document outlines the project-specific architecture, requirements, and development roadmap for the KivyMD Chat App.

## 🎯 Project Overview

A modern, production-ready chat interface built with KivyMD and Material Design 3. Features real-time WebSocket communication, streaming responses, and optimized performance for both desktop Linux and Android deployment.

## 🏗️ Target Architecture

### **Directory Structure**
```
KIVY_CHAT_APP/
├── chat_ui/                     # Main Python package
│   ├── __init__.py
│   ├── app.py                   # App subclass + entry point
│   ├── screens/                 # Individual Screen classes
│   │   ├── __init__.py
│   │   └── chat_screen.py
│   ├── ui/                      # KV files & custom widgets
│   │   ├── __init__.py
│   │   ├── kv/                  # KV layout files
│   │   └── widgets/             # Custom widgets
│   │       └── __init__.py
│   ├── core/                    # WebSockets, config, utilities
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── mobile_config.py
│   │   └── websocket_client.py
│   └── theme.py                 # UI styling & Material Design colors
├── assets/                      # Icons, fonts, other static files
│   ├── icons/
│   └── fonts/
├── main.py                      # launcher: imports and runs chat_ui.app
├── pyproject.toml               # metadata + build-system (setuptools)
├── buildozer.spec               # Android config
└── README.md
```

## 🐍 Technology Stack & Requirements

### **Core Dependencies**
- **Python:** `>=3.10.0,<3.11` (Android Buildozer compatibility constraint)
- **KivyMD:** `~=1.2.0` (Material Design UI)
- **Kivy:** `~=2.3.1` (Cross-platform GUI framework)
- **WebSockets:** `~=13.1` (Real-time backend communication)

### **Development Dependencies**
- **Testing:** `pytest~=8.3.4`, `pytest-asyncio~=0.25.0`
- **Code Quality:** `black~=25.1.0`
- **Package Management:** `uv` (exclusive, no pip/poetry/conda)

### **Build System**
- **Backend:** `setuptools.build_meta`
- **Package Discovery:** Include `chat_ui*`, exclude `assets*`
- **Version Syntax:** Compatible release (`~=`) for stable packages

## 📱 Platform Requirements

### **Desktop Linux**
- **Python:** 3.10.x
- **Dependencies:** System clipboard support (`xclip`, `xsel`)
- **Performance:** 60fps UI, <5% CPU during active chat

### **Android Deployment**
- **Target API:** 35 (Google Play requirement from August 31, 2025)
- **Minimum API:** 21 (broad device compatibility)
- **NDK:** r25b (latest stable)
- **Build Tool:** Buildozer
- **Architecture:** arm64-v8a + armeabi-v7a

### **Performance Targets**
- **Startup time:** ~2-3 seconds
- **Memory usage:** ~50-80MB (depending on message history)
- **Backend SLO:** P95 latency ≤ 100ms
- **UI responsiveness:** 60fps with throttled updates

## 🔧 WebSocket Protocol Specification

### **Backend Integration**
- **Endpoint:** `/ws/chat`
- **Input Format:** `{"message": "user text"}`
- **Response Format:**
  - **Streaming chunks:** `{"type": "chunk", "content": "partial text"}`
  - **Completion signal:** `{"type": "complete"}`
- **Connection Features:**
  - Auto-reconnection with exponential backoff
  - Health monitoring with ping/pong
  - Graceful fallback to demo mode when backend unavailable

### **Configuration via Environment Variables**
```bash
# Connection Settings
export CHAT_WEBSOCKET_URI="ws://localhost:8000/ws/chat"
export CHAT_CONNECTION_TIMEOUT="30.0"
export CHAT_MAX_RETRIES="3"

# Performance Tuning
export CHAT_SCROLL_THROTTLE_MS="100"    # Scroll update frequency
export CHAT_TEXT_BATCH_MS="50"          # Text streaming batches
export CHAT_MAX_MESSAGES="100"          # Message history limit

# UI Customization
export CHAT_APP_TITLE="My Chat App"
export CHAT_AI_NAME="My Assistant"
export CHAT_WINDOW_WIDTH="400"
export CHAT_WINDOW_HEIGHT="600"
```

## 📋 Development Roadmap

### **Phase 1: Core Refactoring** ✅ **COMPLETED**
- [x] Create modular directory structure
- [x] Migrate to setuptools build system
- [x] Fix all import paths for new structure
- [x] Update `pyproject.toml` configuration
- [x] Verify desktop workflow functionality

### **Phase 2: Android Support** 🔄 **IN PROGRESS**
- [ ] Initialize Buildozer configuration (`buildozer init`)
- [ ] Configure `buildozer.spec`:
  - `source.include_exts = py,kv,ttf,otf,png,jpg`
  - `package.name = KivyChatApp`
  - `requirements = python3,kivy==2.3.1,kivymd==1.2.0,websockets`
  - `entrypoint = main.py`
- [ ] Organize assets under `assets/` for bundling
- [ ] Test on Android emulator/device
- [ ] Smoke-test screens, WebSocket connection, theming

### **Phase 3: CI & Quality Assurance** ⏳ **PENDING**
- [ ] **GitHub Actions CI:**
  - Lint on each PR (`ruff --strict`)
  - Type checking (`mypy --strict`)
  - Basic smoke-test: `python main.py --headless`
- [ ] **Testing Infrastructure:**
  - ≥90% line coverage with `pytest`
  - Async testing with `pytest-asyncio`
  - Mobile-specific test scenarios

### **Phase 4: Production Deployment** ⏳ **PENDING**
- [ ] **Google Play Store Preparation:**
  - Build signed release APK/AAB
  - Privacy policy (if app collects data)
  - Store listing and metadata
- [ ] **Security Hardening:**
  - HTTPS/WSS for production connections
  - Certificate pinning implementation
  - Network security configuration
- [ ] **Performance Optimization:**
  - Memory profiling and optimization
  - Network efficiency improvements
  - UI scaling for different screen sizes

## 🧪 Testing Strategy

### **Test Coverage Requirements**
- **Critical Logic:** ≥90% line coverage
- **WebSocket Client:** Connection, reconnection, message handling
- **UI Components:** Screen navigation, message display, user input
- **Mobile Compatibility:** Android lifecycle, touch interactions, keyboard handling

### **Quality Gates**
- `ruff --strict` must pass (with D1xx exceptions for internal code)
- `mypy --strict` must pass (--ignore-missing-imports allowed)
- All tests must pass on both desktop and Android
- Performance benchmarks must meet SLO targets

## 🚀 Deployment Checklist

### **Pre-Release Validation**
- [ ] Test on multiple Android devices/versions (API 21+)
- [ ] Verify WebSocket connections work on mobile networks
- [ ] Check app permissions are minimal and necessary
- [ ] Test offline/demo mode functionality
- [ ] Verify UI scaling on different screen sizes
- [ ] Test keyboard interactions and text input
- [ ] Ensure app handles Android lifecycle properly
- [ ] Check memory usage and performance
- [ ] Test app update scenarios
- [ ] Verify crash reporting works

### **Security Validation**
- [ ] Use HTTPS/WSS for production WebSocket connections
- [ ] Implement certificate pinning for sensitive data
- [ ] Add network security configuration for cleartext traffic
- [ ] Verify app signing key security
- [ ] Audit permissions and data collection practices

## 🎯 Success Metrics

### **Technical Metrics**
- **Build Success Rate:** >95% for both desktop and Android
- **Test Coverage:** ≥90% line coverage maintained
- **Performance:** All SLO targets consistently met
- **Security:** Zero critical vulnerabilities in dependencies

### **User Experience Metrics**
- **App Store Rating:** Target >4.0 stars
- **Crash Rate:** <1% of sessions
- **Connection Success:** >99% WebSocket connection establishment
- **Response Time:** <100ms P95 for backend interactions

## 📚 Documentation Requirements

- [ ] **API Documentation:** WebSocket protocol specification
- [ ] **Deployment Guide:** Step-by-step Android build instructions
- [ ] **Configuration Reference:** All environment variables documented
- [ ] **Troubleshooting Guide:** Common issues and solutions
- [ ] **Contributing Guide:** Development setup and coding standards

---

This plan serves as the living roadmap for the KivyMD Chat App project, balancing technical excellence with practical deployment requirements. 