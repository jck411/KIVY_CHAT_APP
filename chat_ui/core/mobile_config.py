"""
Mobile-specific configuration for Android deployment
"""
import os
from kivy.utils import platform
from kivy.metrics import dp


class MobileConfig:
    """Mobile-specific configuration adjustments"""
    
    # Detect if running on mobile
    IS_MOBILE = platform in ('android', 'ios')
    IS_ANDROID = platform == 'android'
    IS_IOS = platform == 'ios'
    
    @staticmethod
    def get_window_size():
        """Get appropriate window size for platform"""
        if MobileConfig.IS_MOBILE:
            # On mobile, use fullscreen/dynamic sizing
            return None, None
        else:
            # Desktop defaults
            return (
                int(os.getenv("CHAT_WINDOW_WIDTH", "400")),
                int(os.getenv("CHAT_WINDOW_HEIGHT", "600"))
            )
    
    @staticmethod
    def get_spacing():
        """Get touch-friendly spacing for mobile"""
        if MobileConfig.IS_MOBILE:
            return {
                'small': dp(12),
                'medium': dp(16),
                'large': dp(24),
                'xlarge': dp(32)
            }
        else:
            return {
                'small': dp(8),
                'medium': dp(12),
                'large': dp(16),
                'xlarge': dp(24)
            }
    
    @staticmethod
    def get_sizes():
        """Get touch-friendly sizes for mobile"""
        if MobileConfig.IS_MOBILE:
            return {
                'input_height': dp(80),  # Larger for touch
                'header_height': dp(72),
                'button_size': dp(56),   # Material Design minimum touch target
                'avatar_size': dp(48),
                'message_font': dp(16),
                'title_font': dp(20),
                'status_font': dp(14),
                'input_font': dp(16)
            }
        else:
            return {
                'input_height': dp(60),
                'header_height': dp(56),
                'button_size': dp(48),
                'avatar_size': dp(40),
                'message_font': dp(14),
                'title_font': dp(18),
                'status_font': dp(12),
                'input_font': dp(14)
            }
    
    @staticmethod
    def get_websocket_config():
        """Get mobile-optimized WebSocket configuration"""
        if MobileConfig.IS_MOBILE:
            return {
                'ping_interval': 30,      # More frequent on mobile
                'ping_timeout': 10,
                'connection_timeout': 15, # Shorter timeout for mobile networks
                'max_retries': 5,         # More retries for unstable mobile connections
                'retry_delay': 2.0
            }
        else:
            return {
                'ping_interval': 120,
                'ping_timeout': 10,
                'connection_timeout': 30,
                'max_retries': 3,
                'retry_delay': 1.0
            }
    
    @staticmethod
    def configure_for_mobile():
        """Configure app settings for mobile platforms"""
        if MobileConfig.IS_ANDROID:
            # Android-specific configurations
            from kivy.config import Config as KivyConfig
            
            # Disable window configuration on Android (handled by system)
            KivyConfig.remove_option('graphics', 'width')
            KivyConfig.remove_option('graphics', 'height')
            
            # Enable proper keyboard handling
            KivyConfig.set('kivy', 'keyboard_mode', 'systemandmulti')
            
            # Optimize for touch
            KivyConfig.set('input', 'mouse', 'mouse,disable_multitouch')
        
        elif MobileConfig.IS_IOS:
            # iOS-specific configurations
            from kivy.config import Config as KivyConfig
            
            # iOS keyboard handling
            KivyConfig.set('kivy', 'keyboard_mode', 'systemandmulti') 