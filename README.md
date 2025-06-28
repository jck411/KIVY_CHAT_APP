# 💬 KivyMD Chat UI

A modern, production-ready chat interface built with KivyMD and Material Design 3. Features real-time WebSocket communication, streaming responses, and optimized performance for both development and production environments.

## 🌟 Current Features

### **Core Chat Functionality**
- **Real-time messaging** with WebSocket backend integration
- **Streaming AI responses** with live text updates as messages arrive
- **Demo mode** - Works offline with mock responses when backend unavailable
- **Connection state monitoring** with automatic reconnection
- **Message history management** with automatic cleanup for performance

### **User Interface**
- **Material Design 3** with modern, clean aesthetics
- **Responsive chat bubbles** with user/AI message differentiation
- **Real-time status indicators** (Online, Connecting, Demo Mode, etc.)
- **Smooth scrolling** with throttled performance optimization
- **Professional header** with avatar and connection status

### **Performance & Reliability**
- **Text batching** for smooth streaming updates (50ms batches)
- **Scroll throttling** to maintain 60fps during rapid updates
- **Memory management** with configurable message history limits
- **Health monitoring** with ping/pong connection checks
- **Exponential backoff** retry logic for robust connections

## 🏗️ Architecture Overview

### **Key Components**

```
├── main.py                    # App entry point & configuration
├── chat_ui/
│   ├── modern_chat.py        # Main UI screen & chat logic
│   ├── websocket_client.py   # Backend communication layer
│   ├── theme.py             # UI styling & Material Design colors
│   └── config.py            # Centralized configuration management
└── pyproject.toml           # uv package management
```

### **How It Works**

1. **App Initialization** (`main.py`)
   - Configures Kivy settings for optimal performance
   - Suppresses verbose logging for clean production output
   - Sets up Material Design 3 theming

2. **Chat Interface** (`modern_chat.py`)
   - Creates modern UI with responsive chat bubbles
   - Manages message display and user input
   - Handles both real-time and demo modes

3. **WebSocket Communication** (`websocket_client.py`)
   - Maintains persistent connection to backend
   - Implements streaming message reception
   - Provides automatic reconnection with health monitoring

4. **Configuration System** (`config.py`)
   - Environment variable support for all settings
   - Production-optimized defaults
   - Easy customization without code changes

### **Event-Driven Architecture**

The app uses event-driven patterns throughout:
- **Async WebSocket handling** for non-blocking communication
- **Clock-based UI updates** for smooth streaming text
- **Background threading** for connection management
- **Callback-based message handling** for real-time updates

## 🚀 Installation & Setup

### **Prerequisites**
```bash
# System packages (required for clipboard functionality)
sudo apt-get install xclip xsel  # Linux only
```

### **Project Setup**
```bash
# Clone and install dependencies
git clone <your-repo>
cd KIVY_FRONTEND
uv sync
```

## 📱 Usage

### **Basic Usage**
```bash
# Start the chat application
uv run main.py
```

### **Development Mode**
```bash
# Run with verbose logging for debugging
KIVY_LOG_LEVEL=debug uv run main.py
```

### **Production Mode**
The app automatically runs in production mode with:
- Minimal logging output
- Optimized performance settings
- Clean startup without warnings

## ⚙️ Configuration

All settings can be customized via environment variables:

### **Connection Settings**
```bash
export CHAT_WEBSOCKET_URI="ws://localhost:8000/ws/chat"
export CHAT_CONNECTION_TIMEOUT="30.0"
export CHAT_MAX_RETRIES="3"
```

### **Performance Tuning**
```bash
export CHAT_SCROLL_THROTTLE_MS="100"    # Scroll update frequency
export CHAT_TEXT_BATCH_MS="50"          # Text streaming batches
export CHAT_MAX_MESSAGES="100"          # Message history limit
```

### **UI Customization**
```bash
export CHAT_APP_TITLE="My Chat App"
export CHAT_AI_NAME="My Assistant"
export CHAT_WINDOW_WIDTH="400"
export CHAT_WINDOW_HEIGHT="600"
```

## 🔧 Backend Integration

### **WebSocket Protocol**
The app expects a WebSocket server at `/ws/chat` that:
- Accepts JSON messages: `{"message": "user text"}`
- Responds with streaming chunks: `{"type": "chunk", "content": "partial text"}`
- Signals completion with: `{"type": "complete"}`

### **Example Backend Response**
```json
{"type": "chunk", "content": "Hello"}
{"type": "chunk", "content": " there!"}
{"type": "complete"}
```

## 🐛 Troubleshooting

### **Common Issues**

**1. Clipboard Warnings (Linux)**
```bash
# Install required system packages
sudo apt-get install xclip xsel
```

**2. Connection Issues**
- App automatically falls back to demo mode if backend unavailable
- Check `CHAT_WEBSOCKET_URI` environment variable
- Verify backend server is running on expected port

**3. Performance Issues**
- Adjust `CHAT_SCROLL_THROTTLE_MS` for smoother scrolling
- Reduce `CHAT_MAX_MESSAGES` for lower memory usage
- Increase `CHAT_TEXT_BATCH_MS` for less frequent updates

**4. Verbose Logging**
- The app is configured for clean production output
- All KivyMD deprecation warnings are suppressed
- Only essential startup and error messages are shown

### **Debug Mode**
For development, enable verbose logging:
```bash
export KIVY_LOG_LEVEL=debug
export CHAT_CONNECTION_TIMEOUT=5.0
uv run main.py
```

## 🏷️ Tech Stack

- **Python 3.12+** with uv package management
- **KivyMD 2.0.1** for Material Design UI
- **Kivy 2.3.1** for cross-platform GUI framework
- **WebSockets 15.0.1** for real-time backend communication
- **AsyncIO** for non-blocking operations

## 📊 Performance Characteristics

- **Startup time**: ~2-3 seconds
- **Memory usage**: ~50-80MB (depending on message history)
- **CPU usage**: <5% during active chat
- **Network**: Efficient WebSocket with compression support
- **UI responsiveness**: 60fps with throttled updates

## 🎯 Production Ready

This application is designed for production use with:
- ✅ **Error handling** - Graceful fallbacks and user feedback
- ✅ **Resource management** - Automatic cleanup and memory limits
- ✅ **Clean logging** - Minimal noise, essential information only
- ✅ **Performance optimization** - Throttled updates and efficient rendering
- ✅ **Connection resilience** - Auto-reconnection with exponential backoff

---

Built with ❤️ using modern Python practices and Material Design principles. 

---

# 🔧 Project Refactoring Plan

## Developer-Friendly Structure Migration

This section outlines the step-by-step refactoring plan to transform the current structure into a more modular, developer-friendly layout ready for both desktop Linux and Android deployment.

### 📋 Refactoring Checklist

- [x] **1. Create New "refactor" Branch**
  - ✅ Create branch: `git checkout -b refactor/project-layout`
  - ✅ Push to GitHub for team review

- [x] **2. Define Target Layout**
  - ✅ Plan new directory structure:
    ```
    KIVY_CHAT_APP/
    ├── chat_ui/                     # Main Python package
    │   ├── __init__.py
    │   ├── app.py                   # App subclass + entry point
    │   ├── screens/                 # Individual Screen classes
    │   ├── ui/                      # KV files & custom widgets
    │   └── core/                    # WebSockets, config, utilities
    │
    ├── assets/                      # Icons, fonts, other static files
    │   ├── icons/
    │   └── fonts/
    │
    ├── main.py                      # launcher: imports and runs chat_ui.app
    ├── pyproject.toml               # metadata + build-system (swap to setuptools)
    ├── buildozer.spec               # Android config (add later)
    └── README.md
    ```

- [x] **3. Scaffold New Directories**
  - ✅ Create empty folders (`screens/`, `ui/kv/`, `ui/widgets/`, `core/`, `assets/icons`, `assets/fonts`)
  - ✅ Add placeholder `__init__.py` files in each Python package

- [x] **4. Move Code into Modules**
  - ✅ **App & Entry Point:**
    - ✅ Move KivyMDApp subclass to `chat_ui/app.py`
    - ✅ Simplify `main.py` to launcher only
  - ✅ **Screens:**
    - ✅ Move screen classes to `chat_ui/screens/`
    - ✅ Update imports accordingly
  - ✅ **Core Logic:**
    - ✅ Move WebSocket client, config, helpers to `chat_ui/core/`
  - ✅ **UI Assets:**
    - ✅ Move `.kv` files to `chat_ui/ui/kv/` (no KV files in current project)
    - ✅ Custom widgets to `chat_ui/ui/widgets/` (prepared for future use)

- [x] **5. Update Imports & KV Loading**
  - ✅ Fix all import paths for new structure
  - ✅ Update imports for core modules
  - ✅ All imports verified working

- [x] **6. Migrate Build System to Setuptools**
  - ✅ Update `pyproject.toml`:
    ```toml
    [build-system]
    requires = ["setuptools>=65.0", "wheel"]
    build-backend = "setuptools.build_meta"
    ```
  - ✅ Remove `tool.hatch` section
  - ✅ Add package discovery configuration
  - ✅ Update dependencies to use compatible release (~=) syntax
  - ✅ Update Python requirement to >=3.13.0a

- [x] **7. Verify Desktop Workflow**
  - ✅ Test imports with: `uv run python -c "from chat_ui.app import ChatApp"`
  - ✅ Build system works correctly with setuptools
  - ✅ All import paths verified working

- [ ] **8. Add Android Support with Buildozer**
  - Initialize: `buildozer init`
  - Configure `buildozer.spec`:
    - `source.include_exts = py,kv,ttf,otf,png,jpg`
    - `package.name = KivyChatApp`
    - `requirements = python3,kivy==2.3.1,kivymd==1.2.0,websockets`
    - `entrypoint = main.py`
  - Organize assets under `assets/` for bundling

- [ ] **9. Test on Android Emulator / Device**
  - Run: `buildozer android debug deploy run`
  - Smoke-test screens, WebSocket connection, theming

- [ ] **10. Set Up CI & Documentation**
  - **CI (GitHub Actions):**
    - Lint on each PR (`ruff --strict`)
    - Type checking (`mypy --strict`)
    - Basic smoke-test: `python main.py --headless`
  - **Update README:**
    - Document new structure
    - Add "Getting Started" for desktop and Android

- [ ] **11. Review & Merge**
  - Open PR against `main`
  - Team review: directory layout, import correctness, Android testing
  - Merge and delete `refactor/*` branch

### 🎯 Benefits of This Refactoring

- **Clear Separation of Concerns:** UI vs. core logic
- **Easy Packaging & Distribution:** Both Linux & Android ready
- **Scalable Architecture:** Clean addition of new screens, widgets, platforms
- **Developer Experience:** Intuitive structure, easy navigation
- **Production Ready:** CI integration, proper testing setup

### 📝 Notes

- **Package Management:** Continue using `uv` for all dependency management
- **Python Version:** Target Python 3.13.0-alpha as per project standards
- **Testing:** Maintain ≥90% line coverage with `pytest`
- **Performance:** Keep existing SLO targets (P95 latency ≤ 100ms)
 