# 🎬 Watch Party Companion - Nova

**Your AI friend who watches videos with you and actually has personality!**

Nova is a split-screen watch companion that uses local vision AI (Ollama + LLaVA) to watch TikToks, YouTube videos, or any content with you - and she's got *opinions*.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎮 **Real-time vision AI** - Nova actually sees what you're watching using LLaVA 7B
- 💬 **Natural personality** - Casual slang, emojis, sarcasm, and honest reactions
- 👀 **Split-screen design** - Watch on the left, chat with Nova on the right
- 🔥 **Auto-commentary** - Nova comments every 30 seconds on what's happening
- 💯 **Interactive chat** - Ask Nova questions about what's on screen
- 🎯 **Stays in character** - No "I'm an AI" breaking immersion

## 🎬 Screenshot

![Nova in Action](screenshot.png)


*Nova watching and commenting on a video in real-time*

## 🚀 Quick Start

# 🎬 Watch Party Companion - Nova

**Your AI friend who watches videos with you and actually has personality!**

Nova is a split-screen watch companion that uses local vision AI (Ollama + LLaVA) to watch TikToks, YouTube videos, or any content with you - and she's got *opinions*.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 🎮 **Real-time vision AI** - Nova actually sees what you're watching using LLaVA 7B
- 💬 **Natural personality** - Casual slang, emojis, sarcasm, and honest reactions
- 👀 **Split-screen design** - Watch on the left, chat with Nova on the right
- 🔥 **Auto-commentary** - Nova comments every 30 seconds on what's happening
- 💯 **Interactive chat** - Ask Nova questions about what's on screen
- 🎯 **Stays in character** - No "I'm an AI" breaking immersion

## 🎭 Nova's Personality

Nova talks like a real friend:
- Uses varied slang: "ngl", "lowkey", "highkey", "deadass", "fr", "bussin", "no cap"
- Adds emojis naturally: 🔥 💀 😭 👀 ✨ 😏
- Has opinions and isn't afraid to share them
- Appreciates attractive people on screen
- Can be playfully sarcastic
- Keeps responses short and punchy (1-2 sentences)

## 📋 Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- LLaVA model downloaded

## 🚀 Quick Start

### 1. Install Ollama

Download and install from [ollama.ai](https://ollama.ai/)

### 2. Pull the LLaVA model

```bash
ollama pull llava:7b
```

### 3. Install Python dependencies

```bash
pip install pyautogui ollama pillow tkinter --break-system-packages
```

(Note: `--break-system-packages` is needed for some Python environments)

### 4. Run the companion

```bash
python watchparty_v2_3.py
```

### 5. Start watching!

- Open a video on the **left half** of your screen (TikTok, YouTube, etc.)
- Nova's window will appear on the **right half**
- Nova will automatically comment every 30 seconds
- Chat with Nova anytime by typing in the input box!

## 💡 Usage Tips

- **For best results**: Make the video fullscreen on the left half of your screen
- **Nova's cooldown**: She comments every 30 seconds when you're not actively chatting
- **Keep it interactive**: Nova responds better when you engage with her
- **Screenshots saved**: All captured frames are saved in `watch_party_screenshots/` folder

## 🎨 Example Interactions

**You:** "what do you think of this?"  
**Nova:** "Ngl that cinematography is fire 🔥 Lowkey jealous of that lighting"

**You:** "is this cringe?"  
**Nova:** "Lmao yeah a little bit but I'm here for it anyway 😭"

**You:** "who looks better?"  
**Nova:** "Deadass they both look good but left side is giving main character energy ✨"

## 🏗️ Project Evolution

This project went through several iterations to find the perfect balance:

- **v1.x** - Initial attempts, struggled with vision model responses
- **v2.0** - Fixed vision processing with simple, direct prompts
- **v2.1** - Added basic personality (casual friend vibes)
- **v2.2** - More slang and opinions
- **v2.3** - Full personality with emojis, sarcasm, and flirty energy ✨ *(current)*

**Key insight**: Vision models work best with simple, direct prompts. Complex system messages or conversation history can confuse them and trigger generic "I'm an AI" responses.

## 🔧 Technical Details

**Architecture:**
- `pyautogui` for screen capture (left half of screen)
- `ollama` Python library for LLaVA model inference
- `tkinter` for the GUI
- Threading for non-blocking auto-commentary

**Model:**
- LLaVA 7B (via Ollama)
- Processes images + text prompts
- Runs locally on your machine

**Performance:**
- Response time: ~2-5 seconds depending on hardware
- Screenshot capture: ~0.5 seconds
- Memory usage: ~4-6GB RAM (model dependent)

## 🎯 Future Ideas

- [ ] Support for other vision models (GPT-4V, Claude with API)
- [ ] Customizable personality presets
- [ ] Multi-language support
- [ ] Voice output (TTS)
- [ ] Save conversation history
- [ ] Adjustable auto-comment frequency
- [ ] Support for multiple monitors

## 🐛 Troubleshooting

**"Vision model not working" / "I'm an AI language model" responses:**
- Make sure LLaVA is properly installed: `ollama pull llava:7b`
- Try running the test script: `python test_vision.py`
- Restart Ollama service

**Nova's window not staying on top:**
- This is a known issue on some window managers
- Try manually keeping the window on top

**Poor image quality:**
- Ensure video is playing on left half of screen
- Try making the video larger/fullscreen on left side
- Check screenshot samples in `watch_party_screenshots/` folder

## 📝 License

MIT License - feel free to modify and use as you like!

## 🙏 Acknowledgments

- Built with [Ollama](https://ollama.ai/)
- Uses [LLaVA](https://llava-vl.github.io/) vision model
- Inspired by the desire to never watch videos alone again 😄

## 🤝 Contributing

Found a bug? Have an idea? PRs and issues welcome!

---

**Made with 🔥 by someone who wanted an AI friend to watch TikToks with**

## 💫 Let's connect
- 💌 [Email](mailto:marisombra@proton.me)
- 🎮 [Twitch](https://www.twitch.tv/marissombra)    
- 🧵 [TikTok](https://www.tiktok.com/@marissombra)
- 🪩 [Itch.io](https://marisombra.itch.io/) (for games)
 
*Note: Nova is running locally on your machine - no data is sent to external servers!*
