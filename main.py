#!/usr/bin/env python3
"""
KivyMD Chat UI - Production-ready chat interface
Launcher entry point for the application
"""

import sys
from chat_ui.app import ChatApp


def main():
    """Main entry point with error handling"""
    try:
        ChatApp().run()
    except KeyboardInterrupt:
        print("\n👋 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Application failed to start: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 