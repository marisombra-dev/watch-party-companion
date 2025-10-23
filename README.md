# 🎬 Watch Party with Nova

An AI companion that watches videos with you and provides real-time commentary! Nova uses vision AI to see what's on your screen and react naturally like a friend watching alongside you.

## ✨ Features

### Two Modes:

**📝 Text Mode**
- Split-screen interface with live commentary
- Type to chat with Nova about what you're watching
- Text-based interaction

**🎤 Voice Mode** ⭐ NEW!
- Nova speaks her commentary out loud
- High-quality text-to-speech with 5 voice options
- Voice input - talk to Nova using your microphone
- Compact floating window that stays on top

### Nova's Personality
- Playful and slightly sarcastic
- Uses modern slang naturally (lmao, ngl, fr, etc.)
- Adds emojis when they fit the vibe
- Reacts in real-time to what's happening on screen
- Remembers context during your watch session

### Smart Commentary
- Auto-comments every 45 seconds (configurable)
- Waits 15 seconds after you speak before commenting
- Won't interrupt while speaking
- Anti-hallucination prompts for accurate observations
- Vision AI powered by LLaVA

## 🚀 Quick Start

### Prerequisites

```bash
# Core requirements
pip install ollama pyautogui pillow

# For voice mode
pip install edge-tts pygame
pip install SpeechRecognition pyaudio

# Make sure Ollama is installed and running
ollama pull llava:7b
```

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/watch-party-nova.git
cd watch-party-nova
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run Nova:
```bash
python watchparty_voice_final.py
```

## 🎮 How to Use

### Getting Started
1. **Launch the app** - Choose Text Mode or Voice Mode
2. **In Voice Mode**: Select Nova's voice (Aria is default - casual & friendly)
3. **Open a video** anywhere on your screen (YouTube, streaming sites, local videos)
4. **Let Nova watch** - She'll automatically comment every 45 seconds
5. **Interact anytime**:
   - Text Mode: Type in the input box
   - Voice Mode: Press SPACE or click "TALK" button

### Voice Mode Controls
- **SPACE** - Push-to-talk (hold while speaking)
- **TALK Button** - Click to activate voice input
- Status shows what Nova is doing:
  - 🎤 Listening... (capturing your voice)
  - 🤔 Nova is thinking... (generating response)
  - 🎤 Generating voice... (creating audio)
  - Speaking (shows what she's saying)

### Available Voices
Choose from 5 high-quality female voices:
- **Aria** - Casual & Friendly (default) ✨
- **Jenny** - Warm & Conversational
- **Sara** - Professional but friendly
- **Michelle** - Expressive
- **Ashley** - Young & Fun

## ⚙️ Configuration

You can customize Nova's behavior by editing the code:

```python
# Adjust comment frequency (in seconds)
self.comment_cooldown = 45  # Time between auto-comments

# Change how long Nova waits after you speak
time_since_activity >= 15  # Seconds to wait after user input

# Modify personality in prompts
# Look for the prompt strings in get_response() and get_auto_comment()
```

## 🛠️ Technical Details

### How It Works
1. **Screen Capture**: Takes screenshots of the left half of your screen
2. **Vision Analysis**: Sends screenshots to LLaVA (vision language model)
3. **Response Generation**: Creates natural, personality-rich commentary
4. **Voice Synthesis**: Uses Microsoft Edge TTS for high-quality speech
5. **Voice Recognition**: Google Speech Recognition for voice input

### Models Used
- **LLaVA 7B** - Vision language model for understanding video content
- **Edge TTS** - Neural text-to-speech (en-US-AriaNeural and others)
- **Google Speech Recognition** - Voice input processing

### Performance
- **Text Mode**: ~2-3 seconds response time
- **Voice Mode**: ~5-10 seconds (includes TTS generation + audio playback)
- **Screenshot**: Captures left half of screen only
- **Memory**: ~2GB RAM (LLaVA model)

## 📋 System Requirements

- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: Optional (speeds up LLaVA inference)
- **Microphone**: Required for voice input
- **Internet**: Required for voice recognition

## 🐛 Troubleshooting

### "Voice not available"
```bash
pip install edge-tts pygame
```

### "Voice input not available"
```bash
pip install SpeechRecognition pyaudio

# On Linux, you may also need:
sudo apt-get install portaudio19-dev python3-pyaudio

# On macOS:
brew install portaudio
```

### "Ollama not found"
Make sure Ollama is installed and running:
```bash
# Install from https://ollama.ai
ollama serve

# In another terminal:
ollama pull llava:7b
```

### "Nova's responses are too robotic"
The personality prompts are in the `get_response()` and `get_auto_comment()` functions. You can adjust them to make Nova more or less expressive.

### "Window too small / TALK button cut off"
The window should be 320x420 pixels. If it's still too small:
1. Close the app completely
2. Restart it
3. The new size should apply

### "Nova speaks too often / not enough"
Adjust `self.comment_cooldown` (around line 521):
```python
self.comment_cooldown = 45  # Increase = less frequent, decrease = more frequent
```

## 🎨 Customization Ideas

### Change Nova's Personality
Edit the prompts in `get_response()` and `get_auto_comment()` to adjust:
- Sarcasm level
- Slang usage
- Emoji frequency
- Commentary style

### Add More Voices
Edge TTS supports many voices. Add them to `self.available_voices`:
```python
"New Voice Name": "en-US-VoiceCodeNeural",
```

### Adjust Window Position
Edit the geometry line in `setup_voice_mode()`:
```python
self.root.geometry(f"320x420+{x_position}+{y_position}")
```

### Change Screenshot Region
Modify `capture_left_screen()` to capture different areas:
```python
# Currently captures left half:
screenshot = pyautogui.screenshot(region=(0, 0, screen_width//2, screen_height))

# Capture right half instead:
screenshot = pyautogui.screenshot(region=(screen_width//2, 0, screen_width//2, screen_height))
```

## 🤝 Contributing

Contributions are welcome! Some ideas:
- Add more personality options
- Support for other vision models
- Multi-language support
- Video file analysis mode
- Custom voice training
- Persistent memory across sessions
- Export commentary to text file

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) - For easy local LLM deployment
- [LLaVA](https://llava-vl.github.io/) - Vision language model
- [Edge TTS](https://github.com/rany2/edge-tts) - High-quality text-to-speech
- [PyAutoGUI](https://pyautogui.readthedocs.io/) - Screen capture

## 📧 Support

Having issues? Open an issue on GitHub or check the troubleshooting section above!

**Made with 🔥 by someone who wanted an AI friend to watch TikToks with**

## 💫 Let's connect
- 💌 [Email](mailto:marisombra@proton.me)
- 🎮 [Twitch](https://www.twitch.tv/marissombra)    
- 🧵 [TikTok](https://www.tiktok.com/@marissombra)
- 🪩 [Itch.io](https://marisombra.itch.io/) (for games)
 
*Note: Nova is running locally on your machine - no data is sent to external servers!*
---

**Have fun watching with Nova!** 🐿️🎬✨
 
