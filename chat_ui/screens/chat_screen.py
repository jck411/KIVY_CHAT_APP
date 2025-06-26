"""
Modern 2025 Chat Interface - Optimized for production use
"""
import threading
import time
from kivy.clock import Clock
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFabButton
from kivymd.uix.scrollview import MDScrollView

from chat_ui.core.websocket_client import ChatWebSocketClient, ConnectionState
from chat_ui.theme import Colors, Sizes, Spacing, Layout
from chat_ui.core.config import Config, Messages


class ModernBubble(MDCard):
    """Chat message bubble with optimized styling"""
    
    def __init__(self, text, is_user=False, **kwargs):
        super().__init__(**kwargs)
        self.elevation = 0 if is_user else 1
        self.radius = [Sizes.BUBBLE_RADIUS]
        self.size_hint_y = None
        self.adaptive_height = True
        self.padding = [Spacing.MEDIUM, Spacing.SMALL]
        
        if is_user:
            self.theme_bg_color = "Custom"  # Required for KivyMD 2.0+
            self.md_bg_color = Colors.PRIMARY_BLUE
            self.pos_hint = Layout.USER_BUBBLE_POS
            self.size_hint_x = Layout.USER_BUBBLE_WIDTH
            text_color = Colors.TEXT_LIGHT
        else:
            self.theme_bg_color = "Custom"  # Required for KivyMD 2.0+
            self.md_bg_color = Colors.LIGHT_GRAY
            self.pos_hint = Layout.AI_BUBBLE_POS
            self.size_hint_x = Layout.AI_BUBBLE_WIDTH
            text_color = Colors.TEXT_DARK
        
        self.label = MDLabel(
            text=text,
            theme_text_color="Custom",
            text_color=text_color,
            font_size=Sizes.MESSAGE_FONT,
            adaptive_height=True,
            text_size=(dp(300), None),
            markup=True
        )
        self.add_widget(self.label)
    
    def update_text(self, text):
        """Update bubble text content"""
        self.label.text = text


class ModernChatScreen(MDScreen):
    """
    Modern chat interface with streaming support and optimized performance.
    
    Features:
    - Real-time message streaming
    - Scroll throttling for smooth performance
    - Text batching for efficient updates
    - Memory management with message cleanup
    - Connection state monitoring
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = ChatWebSocketClient()
        self.current_bubble = None
        self.backend_available = False
        self.scroll_view = None
        self.connection_monitor_task = None
        
        # Performance optimization variables
        self._scroll_scheduled = False
        self._pending_scroll_event = None
        self._last_scroll_time = 0
        self._scroll_throttle_delay = Config.SCROLL_THROTTLE_MS / 1000.0
        
        # Text batching for streaming optimization
        self._pending_chunks = []
        self._text_update_scheduled = False
        self._text_batch_delay = Config.TEXT_BATCH_MS / 1000.0
        
        # Memory management
        self.max_messages = Config.MAX_MESSAGE_HISTORY
        
        self._setup_ui()
        self._initialize_connection_monitoring()
    
    def _initialize_connection_monitoring(self):
        """Initialize connection testing and monitoring"""
        Clock.schedule_once(self._test_backend, 1.0)
        self.connection_monitor_task = Clock.schedule_interval(self._monitor_connection_state, 2.0)
    
    def _setup_ui(self):
        """Setup the main UI layout and components"""
        layout = MDBoxLayout(
            orientation="vertical",
            theme_bg_color="Custom",  # Required for KivyMD 2.0+
            md_bg_color=Colors.BACKGROUND
        )
        
        # Header with status
        header = self._create_header()
        
        # Messages container with scrolling
        self.messages = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True,
            spacing=Spacing.MEDIUM,
            padding=[Spacing.LARGE, Spacing.LARGE]
        )
        
        self.scroll_view = MDScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            scroll_type=['bars', 'content'],
            bar_width=Layout.SCROLL_BAR_WIDTH
        )
        self.scroll_view.add_widget(self.messages)
        
        # Input area
        input_card = self._create_input_area()
        
        # Add welcome message
        welcome = ModernBubble(Config.WELCOME_MESSAGE)
        self.messages.add_widget(welcome)
        
        # Assemble layout
        layout.add_widget(header)
        layout.add_widget(self.scroll_view)
        layout.add_widget(input_card)
        self.add_widget(layout)
        
        # Initial scroll to bottom
        Clock.schedule_once(lambda dt: self._scroll_to_bottom(force=True), 0.01)
    
    def _create_header(self):
        """Create the header with avatar and status"""
        header = MDCard(
            theme_bg_color="Custom",  # Required for KivyMD 2.0+
            md_bg_color=Colors.WHITE,
            elevation=2,
            radius=[0],
            size_hint_y=None,
            height=Sizes.HEADER_HEIGHT,
            padding=Spacing.MEDIUM
        )
        
        header_content = MDBoxLayout(
            orientation="horizontal",
            spacing=Spacing.SMALL
        )
        
        # Avatar
        avatar = MDCard(
            theme_bg_color="Custom",  # Required for KivyMD 2.0+
            md_bg_color=Colors.PRIMARY_BLUE,
            size_hint=(None, None),
            size=(Sizes.AVATAR_SIZE, Sizes.AVATAR_SIZE),
            radius=[Sizes.BUBBLE_RADIUS]
        )
        
        # Title and status
        title_box = MDBoxLayout(orientation="vertical")
        
        title = MDLabel(
            text=Config.AI_NAME,
            font_size=Sizes.TITLE_FONT,
            bold=True,
            size_hint_y=None,
            height=dp(24)
        )
        
        self.status_label = MDLabel(
            text=Messages.CONNECTING,
            font_size=Sizes.STATUS_FONT,
            theme_text_color="Custom",
            text_color=Colors.TEXT_MUTED,
            size_hint_y=None,
            height=dp(18)
        )
        
        title_box.add_widget(title)
        title_box.add_widget(self.status_label)
        header_content.add_widget(avatar)
        header_content.add_widget(title_box)
        header.add_widget(header_content)
        
        return header
    
    def _create_input_area(self):
        """Create the message input area with send button"""
        input_card = MDCard(
            theme_bg_color="Custom",  # Required for KivyMD 2.0+
            md_bg_color=Colors.WHITE,
            elevation=2,
            radius=[0],
            size_hint_y=None,
            height=Sizes.INPUT_HEIGHT,
            padding=Spacing.MEDIUM
        )
        
        input_layout = MDBoxLayout(
            orientation="horizontal",
            spacing=Spacing.SMALL
        )
        
        self.text_input = MDTextField(
            hint_text="Type your message...",
            multiline=False,
            font_size=Sizes.INPUT_FONT,
            size_hint_x=0.85
        )
        self.text_input.bind(on_text_validate=self.send_message)
        
        send_button = MDFabButton(
            icon="send",
            theme_icon_color="Custom",
            icon_color=Colors.TEXT_LIGHT,
            md_bg_color=Colors.PRIMARY_BLUE,
            size_hint_x=0.15
        )
        send_button.bind(on_release=self.send_message)
        
        input_layout.add_widget(self.text_input)
        input_layout.add_widget(send_button)
        input_card.add_widget(input_layout)
        
        return input_card
    
    def _scroll_to_bottom(self, force=False):
        """Throttled scroll to bottom for smooth performance"""
        current_time = time.time()
        
        if force or (current_time - self._last_scroll_time) >= self._scroll_throttle_delay:
            self._do_scroll()
            self._last_scroll_time = current_time
        elif not self._scroll_scheduled:
            # Schedule a scroll for later if we're throttling
            self._scroll_scheduled = True
            self._pending_scroll_event = Clock.schedule_once(self._do_throttled_scroll, self._scroll_throttle_delay)
    
    def _do_scroll(self):
        """Perform the actual scroll operation"""
        if self.scroll_view:
            self.scroll_view.scroll_y = 0  # Scroll to bottom
    
    def _do_throttled_scroll(self, dt):
        """Execute a throttled scroll operation"""
        self._scroll_scheduled = False
        self._do_scroll()
        self._last_scroll_time = time.time()
    
    def _test_backend(self, dt):
        """Test if backend is available"""
        threading.Thread(target=self._threaded_test, daemon=True).start()
    
    def _threaded_test(self):
        """Test backend availability in a separate thread"""
        try:
            test_success = self.client.test_connection()
            Clock.schedule_once(lambda dt: setattr(self, 'backend_available', test_success))
            if test_success:
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', Messages.ONLINE))
            else:
                Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', Messages.DEMO_MODE))
        except Exception:
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', Messages.DEMO_MODE))
    
    def _monitor_connection_state(self, dt):
        """Monitor and update connection state"""
        if hasattr(self.client, 'connection_state'):
            state = self.client.connection_state
            
            status_map = {
                ConnectionState.DISCONNECTED: Messages.OFFLINE,
                ConnectionState.CONNECTING: Messages.CONNECTING,
                ConnectionState.CONNECTED: Messages.ONLINE,
                ConnectionState.ERROR: Messages.CONNECTION_ERROR,
                ConnectionState.RECONNECTING: Messages.RECONNECTING
            }
            
            new_status = status_map.get(state, Messages.DEMO_MODE)
            if self.status_label.text != new_status:
                self.status_label.text = new_status
                
            # Update backend availability based on connection state
            self.backend_available = (state == ConnectionState.CONNECTED)
        
        # Update demo mode status if backend is not available
        elif not self.backend_available and self.status_label.text != Messages.DEMO_MODE:
            self.status_label.text = Messages.DEMO_MODE
    
    def send_message(self, instance):
        """Handle message sending with backend/demo mode logic"""
        message_text = self.text_input.text.strip()
        if not message_text:
            return
        
        # Clear input immediately for better UX
        self.text_input.text = ""
        
        # Add user message bubble
        user_bubble = ModernBubble(message_text, is_user=True)
        self.messages.add_widget(user_bubble)
        self._scroll_to_bottom()
        
        # Clean up old messages if needed
        self._cleanup_old_messages()
        
        # Send to backend or show demo response
        if self.backend_available:
            self._send_to_backend(message_text)
        else:
            self._show_demo_response(message_text)
    
    def _send_to_backend(self, message):
        """Send message to real backend"""
        threading.Thread(target=self._threaded_send, args=(message,), daemon=True).start()
    
    def _show_demo_response(self, message):
        """Show a demo response when backend is unavailable"""
        demo_text = f"Demo response to: '{message[:30]}{'...' if len(message) > 30 else ''}'"
        ai_bubble = ModernBubble(demo_text)
        self.messages.add_widget(ai_bubble)
        self._scroll_to_bottom()
    
    def _threaded_send(self, message):
        """Send message in separate thread"""
        try:
            self.client.send_message(message, self._on_chunk, self._on_message_complete)
        except Exception as e:
            error_msg = self._format_error_message(str(e))
            Clock.schedule_once(lambda dt: self._show_error_message(error_msg))
    
    def _show_error_message(self, error_msg):
        """Display error message in chat"""
        error_bubble = ModernBubble(f"❌ {error_msg}")
        self.messages.add_widget(error_bubble)
        self._scroll_to_bottom()
        
        # Also update status to show connection issues
        self.status_label.text = Messages.CONNECTION_ERROR
        self.backend_available = False
    
    def _format_error_message(self, error: str) -> str:
        """Format error message for user display"""
        if "Connection refused" in error:
            return "Cannot connect to server. Please check your connection."
        elif "timeout" in error.lower():
            return "Request timed out. Please try again."
        elif "websocket" in error.lower():
            return "Connection lost. Switching to demo mode."
        else:
            return "Something went wrong. Please try again."
    
    def _on_chunk(self, chunk):
        """Handle streaming chunk - use batching for performance"""
        self._pending_chunks.append(chunk)
        
        if not self._text_update_scheduled:
            self._text_update_scheduled = True
            Clock.schedule_once(self._process_batched_chunks, self._text_batch_delay)
    
    def _process_batched_chunks(self, dt):
        """Process all pending chunks in a batch for better performance"""
        if not self._pending_chunks:
            self._text_update_scheduled = False
            return
        
        # Combine all pending chunks
        combined_text = ''.join(self._pending_chunks)
        self._pending_chunks.clear()
        
        self._append_chunk_batch(combined_text)
        self._text_update_scheduled = False
    
    def _on_message_complete(self):
        """Handle message completion"""
        self.current_bubble = None
        Clock.schedule_once(lambda dt: self._focus_input())
    
    def _focus_input(self):
        """Focus the input field for next message"""
        self.text_input.focus = True
    
    def _cleanup_old_messages(self):
        """Remove old messages to prevent memory issues"""
        if len(self.messages.children) > self.max_messages:
            # Remove oldest messages (they're at the end of children list due to how Kivy works)
            messages_to_remove = len(self.messages.children) - self.max_messages
            for _ in range(messages_to_remove):
                if self.messages.children:
                    self.messages.remove_widget(self.messages.children[-1])
    
    def _append_chunk_batch(self, text):
        """Append a batch of text chunks to current message"""
        if not self.current_bubble:
            self.current_bubble = ModernBubble("")
            self.messages.add_widget(self.current_bubble)
        
        # Update the bubble text
        current_text = self.current_bubble.label.text
        self.current_bubble.update_text(current_text + text)
        self._scroll_to_bottom() 