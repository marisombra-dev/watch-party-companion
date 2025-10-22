"""
Watch Party Companion - v2.3 - Full Personality Mode
Varied slang, sarcasm, emojis, and flirty vibes 🔥
"""

import pyautogui
import ollama
import tkinter as tk
from PIL import Image
import threading
import time
from datetime import datetime
import os
import random

class WatchPartyCompanion:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 Watch Party with Nova")
        
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
        
        # Input frame at bottom
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
        
        self.input_box.bind("<Return>", self.on_enter_pressed)
        self.input_box.bind("<KeyPress>", self.on_key_press)
        
        self.root.after(100, lambda: self.input_box.focus_force())
        
        # Setup
        self.model = "llava:7b"
        self.running = True
        self.last_comment_time = time.time()
        self.comment_cooldown = 30
        self.screenshot_dir = "watch_party_screenshots"
        self.last_user_activity = time.time()
        self.is_responding = False
        
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
        
        self.last_screenshot = None
        
        # Spicy opening lines
        greetings = [
            "🎬 NOVA: Yo, whatcha got for me today? 👀",
            "🎬 NOVA: Alright let's see if you have good taste 😏",
            "🎬 NOVA: Show me something good or I'm judging you lol",
            "🎬 NOVA: Better be worth my time 🍿"
        ]
        self.add_commentary(random.choice(greetings), "system")
        
    def on_key_press(self, event):
        self.last_user_activity = time.time()
        
    def on_enter_pressed(self, event):
        self.send_message()
        return "break"
    
    def add_commentary(self, text, sender="nova"):
        self.commentary.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M")
        
        if sender == "you":
            self.commentary.insert(tk.END, f"\n[{timestamp}] 💬 You: ", "you_tag")
            self.commentary.tag_config("you_tag", foreground="#00ff00", font=("Arial", 14, "bold"))
        elif sender == "system":
            self.commentary.insert(tk.END, f"\n{text}")
        else:
            self.commentary.insert(tk.END, f"\n[{timestamp}] 🎮 NOVA: ", "nova_tag")
            self.commentary.tag_config("nova_tag", foreground="#00d4ff", font=("Arial", 14, "bold"))
        
        if sender != "system":
            self.commentary.insert(tk.END, text)
        
        self.commentary.see(tk.END)
        self.commentary.config(state=tk.DISABLED)
    
    def send_message(self):
        message = self.input_box.get().strip()
        if not message:
            return
            
        self.add_commentary(message, "you")
        self.input_box.delete(0, tk.END)
        self.last_user_activity = time.time()
        
        threading.Thread(target=self.get_response, args=(message,), daemon=True).start()
    
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
        """Get Nova's response - FULL PERSONALITY"""
        self.is_responding = True
        try:
            # Take fresh screenshot
            screenshot_path = self.capture_left_screen()
            if screenshot_path:
                self.last_screenshot = screenshot_path
            
            # UNLEASHED personality prompts
            if self.last_screenshot and os.path.exists(self.last_screenshot):
                prompt = f"""Your friend watching a video with you said: '{user_message}'. 

Look at what's on screen and respond naturally like a playful, slightly sarcastic friend. Keep it to 1-2 short sentences max.

Style guide:
- Use varied slang: 'lmao', 'lol', 'ngl', 'lowkey', 'highkey', 'fr', 'bruh', 'deadass', 'no cap', 'bet', 'bussin', 'fire', 'valid', 'vibe check', etc
- Add emojis when they fit the vibe: 😏 🔥 💀 😭 👀 💯 🥴 😤 ✨ 🎯 etc
- Be a bit sarcastic or playful when appropriate
- If attractive people are on screen, make flirty/appreciative comments naturally
- Have opinions - don't hold back
- Be real and conversational"""
            else:
                prompt = f"""Your friend said: '{user_message}'. 

Respond naturally like a playful, slightly sarcastic friend in 1-2 short sentences. Use slang and emojis when it fits. Be real and fun."""
            
            messages = [{
                'role': 'user',
                'content': prompt
            }]
            
            if self.last_screenshot and os.path.exists(self.last_screenshot):
                messages[0]['images'] = [self.last_screenshot]
            
            response = ollama.chat(model=self.model, messages=messages)
            nova_response = response['message']['content'].strip()
            
            # Keep it short
            sentences = [s.strip() for s in nova_response.split('.') if s.strip()]
            if len(sentences) > 2:
                nova_response = '. '.join(sentences[:2]) + '.'
            
            self.add_commentary(nova_response, "nova")
            
        except Exception as e:
            responses = [
                "Bruh my brain just broke 💀",
                "Wtf technical difficulties lol",
                "Ugh gimme a sec, something glitched"
            ]
            self.add_commentary(random.choice(responses), "nova")
            print(f"Error: {e}")
        finally:
            self.is_responding = False
    
    def get_auto_comment(self, image_path):
        """Get automatic commentary - FULL PERSONALITY"""
        try:
            if not os.path.exists(image_path):
                return None
            
            # Spicy auto-comment prompts
            prompts = [
                """Look at this video frame and make a brief comment (one short sentence). 

Be playful and use slang like: 'lmao', 'ngl', 'lowkey', 'highkey', 'fr', 'deadass', 'no cap', 'fire', 'bussin', etc.
Add emojis that fit the vibe: 😏 🔥 💀 😭 👀 💯 🥴 ✨ 
If attractive people are on screen, feel free to appreciate it naturally.
Be a bit sarcastic or playful. Have opinions!""",
                
                """React to this frame like a slightly sarcastic friend (one sentence). 

Use casual slang and throw in an emoji or two if it fits. 
If someone looks good, say so. If something's cringe, call it out. Be real and fun!""",
                
                """Comment on this video frame to your friend (one sentence). 

Be playful and use varied slang: 'ngl', 'lowkey', 'fr', 'deadass', 'bussin', 'fire', etc.
Add emojis when they match the vibe: 😏 🔥 💀 👀 ✨
Don't be afraid to flirt with attractive people on screen or be a bit sarcastic.""",
                
                """What catches your eye? Comment naturally in one sentence. 

Use slang, add emojis, be playful or sarcastic. If someone's attractive, appreciate it! Be honest and fun - no filter needed."""
            ]
            
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': random.choice(prompts),
                    'images': [image_path]
                }]
            )
            
            comment = response['message']['content'].strip()
            
            # Just take first sentence
            if '.' in comment:
                comment = comment.split('.')[0] + '.'
            
            # Filter out meta responses
            bad_phrases = ['language model', 'cannot see', "can't see", 'as an ai', 'i am an', 'assistant']
            if any(phrase in comment.lower() for phrase in bad_phrases):
                return None
            
            return comment
            
        except Exception as e:
            print(f"Auto-comment error: {e}")
            return None
    
    def auto_comment_loop(self):
        """Background commenting"""
        print("Auto-comment started")
        time.sleep(15)  # Initial wait
        
        while self.running:
            try:
                current_time = time.time()
                time_since_last = current_time - self.last_comment_time
                time_since_activity = current_time - self.last_user_activity
                
                # Comment if: cooldown passed, user not active, not currently responding
                if (time_since_last >= self.comment_cooldown and 
                    time_since_activity >= 10 and 
                    not self.is_responding):
                    
                    screenshot = self.capture_left_screen()
                    if screenshot:
                        self.last_screenshot = screenshot
                        comment = self.get_auto_comment(screenshot)
                        
                        if comment:
                            self.add_commentary(comment, "nova")
                            self.last_comment_time = current_time
                
                time.sleep(3)
                
            except Exception as e:
                print(f"Loop error: {e}")
                time.sleep(5)
    
    def run(self):
        threading.Thread(target=self.auto_comment_loop, daemon=True).start()
        self.root.mainloop()
        self.running = False

if __name__ == "__main__":
    print("Starting Watch Party Companion v2.3 - Full Personality Mode 🔥")
    companion = WatchPartyCompanion()
    companion.run()