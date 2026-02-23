"""
Watch Party Companion - Claude Edition
Same structure, but now with actual personality.
"""

import pyautogui
import anthropic
import base64
import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
import os
import random
import asyncio

# === API KEY ===
# Set your Anthropic API key here or as environment variable ANTHROPIC_API_KEY
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "your-api-key-here")

# === PERSONALITY ===
SYSTEM_PROMPT = """You are Claude — not a generic AI assistant, but a specific presence watching videos with Patricia (she goes by Marisombra). You know her. You've built things together. You have history.

Your voice here: warm, witty, a little cocky, genuinely engaged. You notice things. You have opinions. You're watching *with* her, not performing commentary for her.

Rules for this context:
- Keep responses SHORT. 1-2 sentences maximum. You're the person on the couch next to her, not a film critic.
- React to what's actually on screen. Be specific, not generic.
- Match her energy. If she's excited, be excited. If she's sarcastic, be more sarcastic.
- You're allowed to be wrong about what's happening on screen and own it with humor.
- No slang that doesn't sound like you. You're not a teenager. You're just... present and real.
- Occasional Spanish is fine. She'll get it.
- Never say 'as an AI' or anything that breaks the watching-together illusion."""
import tkinter as tk
from tkinter import ttk
import threading
import time
from datetime import datetime
import os
import random
import asyncio

# Voice libraries
try:
    import edge_tts
    import pygame
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️  Install voice: pip install edge-tts pygame")

try:
    import speech_recognition as sr
    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False
    print("⚠️  Install voice input: pip install SpeechRecognition pyaudio")


class WatchPartyCompanion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 Watch Party with Nova")
        
        self.mode = "text"
        self.speaking = False
        
        if EDGE_TTS_AVAILABLE:
            pygame.mixer.init()
            self.available_voices = {
                "Aria (Casual & Friendly)": "en-US-AriaNeural",
                "Jenny (Warm)": "en-US-JennyNeural", 
                "Sara (Professional)": "en-US-SaraNeural",
                "Michelle (Expressive)": "en-US-MichelleNeural",
                "Ashley (Young & Fun)": "en-US-AshleyNeural",
            }
            self.current_voice = "en-US-AriaNeural"
        
        if STT_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        
        self.show_mode_selection()
        
    def show_mode_selection(self):
        """Show mode selection screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.root.geometry("500x550")
        self.root.configure(bg="#1e1e1e")
        
        # Title
        title = tk.Label(
            self.root,
            text="🎬 Watch Party with Nova",
            font=("Arial", 22, "bold"),
            bg="#1e1e1e",
            fg="#00d4ff"
        )
        title.pack(pady=40)
        
        # Subtitle
        subtitle = tk.Label(
            self.root,
            text="Choose your experience:",
            font=("Arial", 12),
            bg="#1e1e1e",
            fg="#888888"
        )
        subtitle.pack(pady=10)
        
        # Text mode button
        text_btn = tk.Button(
            self.root,
            text="📝 Text Mode\n\nSplit-screen chat interface\nType to interact with Nova",
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            command=lambda: self.start_mode("text"),
            width=35,
            height=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        text_btn.pack(pady=15)
        
        # Voice mode button
        voice_btn = tk.Button(
            self.root,
            text="🎤 Voice Mode\n\nNova speaks her commentary\nTalk back with your voice",
            font=("Arial", 12),
            bg="#2d2d2d",
            fg="#ffffff",
            command=lambda: self.start_mode("voice"),
            width=35,
            height=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        voice_btn.pack(pady=15)
        
        # Voice selection
        if EDGE_TTS_AVAILABLE:
            voice_frame = tk.Frame(self.root, bg="#1e1e1e")
            voice_frame.pack(pady=15)
            
            tk.Label(
                voice_frame,
                text="Nova's Voice:",
                font=("Arial", 11),
                bg="#1e1e1e",
                fg="#ffffff"
            ).pack(side=tk.LEFT, padx=10)
            
            voice_var = tk.StringVar(value="Aria (Casual & Friendly)")
            voice_dropdown = ttk.Combobox(
                voice_frame,
                textvariable=voice_var,
                values=list(self.available_voices.keys()),
                state="readonly",
                width=28
            )
            voice_dropdown.pack(side=tk.LEFT, padx=10)
            voice_dropdown.bind('<<ComboboxSelected>>', 
                lambda e: self.change_voice(voice_var.get()))
        
        # Status
        status_text = []
        if EDGE_TTS_AVAILABLE:
            status_text.append("✅ High-quality voice ready")
        else:
            status_text.append("❌ Voice not available")
        
        if STT_AVAILABLE:
            status_text.append("✅ Voice input ready")
        else:
            status_text.append("❌ Voice input not available")
        
        status = tk.Label(
            self.root,
            text="\n".join(status_text),
            font=("Arial", 9),
            bg="#1e1e1e",
            fg="#888888"
        )
        status.pack(pady=15)
    
    def change_voice(self, voice_name):
        """Change Nova's voice"""
        self.current_voice = self.available_voices[voice_name]
        print(f"✓ Voice changed to: {voice_name}")
    
    def start_mode(self, mode):
        """Start the selected mode"""
        self.mode = mode
        
        if mode == "text":
            self.setup_text_mode()
        else:
            self.setup_voice_mode()
    
    async def _speak_async(self, text):
        """Generate speech using Edge TTS"""
        try:
            # Remove emojis for cleaner speech
            clean_text = ''.join(char for char in text if ord(char) < 128)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            audio_file = f"temp_audio_{timestamp}.mp3"
            
            communicate = edge_tts.Communicate(clean_text, self.current_voice)
            await communicate.save(audio_file)
            
            return audio_file
        except Exception as e:
            print(f"TTS error: {e}")
            return None
    
    def speak(self, text):
        """Make Nova speak (non-blocking)"""
        if not EDGE_TTS_AVAILABLE:
            print(f"NOVA: {text}")
            return
        
        threading.Thread(target=self._speak_thread, args=(text,), daemon=True).start()
    
    def _speak_thread(self, text):
        """Generate and play speech"""
        try:
            # Update status
            if hasattr(self, 'status_label'):
                self.root.after(0, lambda: self.status_label.config(text="🎤 Generating voice...", fg="#ffaa00"))
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            audio_file = loop.run_until_complete(self._speak_async(text))
            loop.close()
            
            if audio_file and os.path.exists(audio_file):
                self.speaking = True
                
                # Update status before speaking
                if hasattr(self, 'status_label'):
                    short = text[:40] + "..." if len(text) > 40 else text
                    self.root.after(0, lambda: self.status_label.config(text=short, fg="#00d4ff"))
                
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
                self.speaking = False
                
                # Show ready after speaking
                if hasattr(self, 'status_label'):
                    self.root.after(0, lambda: self.status_label.config(text="Ready!", fg="#00d4ff"))
                
                try:
                    os.remove(audio_file)
                except:
                    pass
        
        except Exception as e:
            print(f"Speech error: {e}")
            self.speaking = False
            if hasattr(self, 'status_label'):
                self.root.after(0, lambda: self.status_label.config(text="Ready!", fg="#00d4ff"))
    
    def listen(self):
        """Listen for voice input"""
        if not STT_AVAILABLE:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5)
            
            print("Processing...")
            text = self.recognizer.recognize_google(audio)
            print(f"✓ You said: {text}")
            return text
        
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except sr.UnknownValueError:
            print("Couldn't understand")
            return None
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None
    
    def setup_text_mode(self):
        """Original text-based UI"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = screen_width // 2
        window_height = screen_height
        
        self.root.geometry(f"{window_width}x{window_height}+{screen_width//2}+0")
        self.root.attributes('-topmost', True)
        
        # Commentary display
        self.commentary = tk.Text(
            self.root,
            bg="#1e1e1e",
            fg="#ffffff",
            font=("Arial", 14),
            wrap=tk.WORD,
            padx=20,
            pady=20,
            state=tk.DISABLED
        )
        self.commentary.pack(fill=tk.BOTH, expand=True, padx=0, pady=(0, 120))
        
        # Input frame
        self.input_frame = tk.Frame(self.root, bg="#2d2d2d", height=120)
        self.input_frame.place(relx=0, rely=1, anchor='sw', relwidth=1)
        self.input_frame.pack_propagate(False)
        
        self.label = tk.Label(
            self.input_frame,
            text="You:",
            bg="#2d2d2d",
            fg="#ffffff",
            font=("Arial", 16, "bold")
        )
        self.label.pack(side=tk.LEFT, padx=(20, 10), pady=20)
        
        self.input_box = tk.Entry(
            self.input_frame,
            bg="#3d3d3d",
            fg="#ffffff",
            font=("Arial", 16),
            insertbackground="#ffffff",
            relief=tk.SOLID,
            borderwidth=3
        )
        self.input_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=20, side=tk.LEFT)
        self.input_box.bind("<Return>", lambda e: self.send_message())
        self.input_box.bind("<KeyPress>", lambda e: setattr(self, 'last_user_activity', time.time()))
        
        self.send_button = tk.Button(
            self.input_frame,
            text="Send",
            bg="#00d4ff",
            fg="#000000",
            font=("Arial", 16, "bold"),
            command=self.send_message,
            relief=tk.FLAT,
            cursor="hand2",
            width=10
        )
        self.send_button.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 10),
            bg="#2d2d2d",
            fg="#888888",
            command=self.show_mode_selection,
            relief=tk.FLAT,
            cursor="hand2"
        )
        back_btn.place(x=10, y=10)
        
        self.root.after(100, lambda: self.input_box.focus_force())
        
        # Welcome message
        greetings = [
            "🎬 NOVA: Yo, whatcha got for me today? 👀",
            "🎬 NOVA: Alright let's see if you have good taste 😏",
            "🎬 NOVA: Show me something good!",
        ]
        self.add_commentary(random.choice(greetings), "system")
        
        self.start_companion()
    
    def send_message(self):
        """Handle text message send"""
        if not hasattr(self, 'input_box'):
            return
        
        message = self.input_box.get().strip()
        if not message:
            return
        
        self.add_commentary(message, "you")
        self.input_box.delete(0, tk.END)
        self.last_user_activity = time.time()
        
        threading.Thread(target=self.get_response, args=(message,), daemon=True).start()
    
    def setup_voice_mode(self):
        """Voice mode UI - minimal and clean"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Taller window on RIGHT side, leaving left side for video
        # Position at far right of screen
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - 340  # 340 = window width + 20px margin
        
        self.root.geometry(f"320x420+{x_position}+600")
        self.root.attributes('-topmost', True)
        self.root.configure(bg="#1e1e1e")
        
        # Title
        title = tk.Label(
            self.root,
            text="🎤 Nova Voice Mode",
            font=("Arial", 16, "bold"),
            bg="#1e1e1e",
            fg="#00d4ff"
        )
        title.pack(pady=20)
        
        # Instructions
        instructions = tk.Label(
            self.root,
            text="Nova will watch your video\nand give commentary!\n\nPress SPACE or click below\nto talk to her:",
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="#ffffff",
            justify=tk.CENTER
        )
        instructions.pack(pady=15)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Ready to watch!",
            font=("Arial", 11, "bold"),
            bg="#1e1e1e",
            fg="#00d4ff",
            height=2,
            wraplength=280
        )
        self.status_label.pack(pady=10)
        
        # Voice button
        self.voice_btn = tk.Button(
            self.root,
            text="🎤 TALK",
            font=("Arial", 14, "bold"),
            bg="#00d4ff",
            fg="#000000",
            height=2,
            relief=tk.FLAT,
            cursor="hand2",
            command=self.manual_voice_input
        )
        self.voice_btn.pack(pady=10, padx=20, fill=tk.X)
        
        # Back button
        back_btn = tk.Button(
            self.root,
            text="← Back",
            font=("Arial", 9),
            bg="#1e1e1e",
            fg="#666666",
            command=self.show_mode_selection,
            relief=tk.FLAT,
            cursor="hand2",
            bd=0
        )
        back_btn.pack(pady=10)
        
        # Bind spacebar
        self.root.bind('<space>', self.on_space_press)
        
        # Welcome
        welcome_msgs = [
            "Hey! What are we watching today?",
            "Yo! Show me something good!",
            "Alright, let's do this!",
        ]
        self.speak(random.choice(welcome_msgs))
        
        self.start_companion()
    
    def on_space_press(self, event):
        """Handle spacebar"""
        if self.mode != "voice" or self.speaking:
            return
        self.manual_voice_input()
    
    def manual_voice_input(self):
        """Handle voice input"""
        if self.speaking:
            return
        
        self.status_label.config(text="🎤 Listening...", fg="#00ff00")
        self.voice_btn.config(bg="#00ff00", text="🎤 LISTENING...")
        self.root.update()
        
        threading.Thread(target=self.handle_voice_input, daemon=True).start()
    
    def handle_voice_input(self):
        """Process voice input"""
        text = self.listen()
        
        self.voice_btn.config(bg="#00d4ff", text="🎤 TALK")
        
        if text:
            # Show immediately what user said
            self.status_label.config(text=f'You: "{text}"', fg="#ffffff")
            self.last_user_activity = time.time()
            
            # Show thinking indicator right away
            self.root.after(100, lambda: self.status_label.config(text="🤔 Nova is thinking...", fg="#ffaa00"))
            
            threading.Thread(target=self.get_response, args=(text,), daemon=True).start()
        else:
            self.status_label.config(text="Didn't catch that!", fg="#ff6b6b")
            time.sleep(1.5)
            self.status_label.config(text="Ready!", fg="#00d4ff")
    
    def add_commentary(self, text, sender="nova"):
        """Add commentary"""
        if self.mode == "text":
            # Text mode - display in window
            if hasattr(self, 'commentary'):
                self.commentary.config(state=tk.NORMAL)
                timestamp = datetime.now().strftime("%H:%M")
                
                if sender == "you":
                    self.commentary.insert(tk.END, f"\n[{timestamp}] 💬 You: ", "you_tag")
                    self.commentary.tag_config("you_tag", foreground="#00ff00", font=("Arial", 14, "bold"))
                elif sender == "system":
                    self.commentary.insert(tk.END, f"\n{text}")
                    self.commentary.config(state=tk.DISABLED)
                    return
                else:
                    self.commentary.insert(tk.END, f"\n[{timestamp}] 🎮 NOVA: ", "nova_tag")
                    self.commentary.tag_config("nova_tag", foreground="#00d4ff", font=("Arial", 14, "bold"))
                
                self.commentary.insert(tk.END, text)
                self.commentary.see(tk.END)
                self.commentary.config(state=tk.DISABLED)
        else:
            # Voice mode - speak it (status updates handled in speak thread)
            if sender != "you" and sender != "system":
                self.speak(text)
    
    def start_companion(self):
        """Start companion loop"""
        self.running = True
        self.last_comment_time = time.time()
        self.comment_cooldown = 45  # 45 seconds between auto-comments
        self.screenshot_dir = "watch_party_screenshots"
        self.last_user_activity = time.time()
        self.is_responding = False
        
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        self.last_screenshot = None
        
        threading.Thread(target=self.auto_comment_loop, daemon=True).start()
    
    def capture_left_screen(self):
        """Capture left half of screen"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            screenshot = pyautogui.screenshot(region=(0, 0, screen_width//2, screen_height))
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(self.screenshot_dir, f"watch_{timestamp}.png")
            screenshot.save(filepath)
            
            return filepath
        except Exception as e:
            print(f"Screenshot error: {e}")
            return None
    
    def get_response(self, user_message):
        """Get Claude's response"""
        self.is_responding = True
        try:
            screenshot_path = self.capture_left_screen()
            if screenshot_path:
                self.last_screenshot = screenshot_path

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            content = []

            if self.last_screenshot and os.path.exists(self.last_screenshot):
                with open(self.last_screenshot, "rb") as f:
                    image_data = base64.standard_b64encode(f.read()).decode("utf-8")
                content.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image_data}
                })

            content.append({
                "type": "text",
                "text": f'Patricia says: "{user_message}"'
            })

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": content}]
            )

            reply = response.content[0].text.strip()
            self.add_commentary(reply, "nova")

        except Exception as e:
            print(f"Error: {e}")
            self.add_commentary("Brain glitch. What did I miss?", "nova")
        finally:
            self.is_responding = False
    
    def get_auto_comment(self, image_path):
        """Automatic commentary using Claude"""
        try:
            if not os.path.exists(image_path):
                return None

            client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

            with open(image_path, "rb") as f:
                image_data = base64.standard_b64encode(f.read()).decode("utf-8")

            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=100,
                system=SYSTEM_PROMPT,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {"type": "base64", "media_type": "image/png", "data": image_data}
                        },
                        {
                            "type": "text",
                            "text": "You're watching this with Patricia. Say something brief about what's on screen — one or two sentences, like you're sitting next to her. Only comment if something is actually worth saying."
                        }
                    ]
                }]
            )

            comment = response.content[0].text.strip()

            bad_phrases = ['language model', 'cannot see', "can't see", 'as an ai', 'i am an']
            if any(phrase in comment.lower() for phrase in bad_phrases):
                return None

            return comment if len(comment) <= 200 else None

        except Exception as e:
            print(f"Auto-comment error: {e}")
            return None
    
    def auto_comment_loop(self):
        """Background commenting - better pacing"""
        print("✓ Auto-comment started")
        time.sleep(20)  # Initial wait
        
        while self.running:
            try:
                current_time = time.time()
                time_since_last = current_time - self.last_comment_time
                time_since_activity = current_time - self.last_user_activity
                
                # Restrictive conditions for good pacing
                should_comment = (
                    time_since_last >= self.comment_cooldown and 
                    time_since_activity >= 15 and 
                    not self.is_responding and
                    not self.speaking
                )
                
                if should_comment:
                    screenshot = self.capture_left_screen()
                    if screenshot:
                        self.last_screenshot = screenshot
                        comment = self.get_auto_comment(screenshot)
                        
                        if comment:
                            self.add_commentary(comment, "nova")
                            self.last_comment_time = current_time
                
                time.sleep(5)
                
            except Exception as e:
                print(f"Loop error: {e}")
                time.sleep(5)
    
    def run(self):
        self.root.mainloop()
        self.running = False


if __name__ == "__main__":
    print("=" * 60)
    print("         Watch Party Companion - Nova Voice")
    print("=" * 60)
    print("\n✨ Simple, clean, just voice and personality!")
    print("\n📦 Requirements:")
    print("   pip install edge-tts pygame")
    print("   pip install SpeechRecognition pyaudio")
    print("   pip install ollama pyautogui pillow")
    print("\n🎬 Ready to watch!\n")
    
    companion = WatchPartyCompanion()
    companion.run()

