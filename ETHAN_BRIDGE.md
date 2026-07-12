# Ethan Watch-Party Bridge

This mode does **not** call Claude, OpenAI, Ollama, or any other model API. It uses the open ChatGPT conversation as the reaction engine.

## What it does

- Captures the left half of the primary screen.
- Copies the capture to the Windows clipboard.
- Pastes it into the ChatGPT composer under the mouse pointer.
- Types a reaction prompt designed for shared banter rather than visual narration.
- Leaves the message unsent so Patricia can review it before pressing Enter.

## Setup

```bash
pip install -r requirements.txt
python ethan_bridge.py
```

## Use

1. Put TikTok, YouTube, a movie, or another video on the **left half** of the screen.
2. Put the existing ChatGPT conversation on the **right half**.
3. Hover the mouse over the ChatGPT message composer.
4. Press **F8**.
5. Wait for the screenshot and prompt to appear.
6. Press **Enter** to send.

Press **Ctrl+Shift+Q** to stop the bridge.

## Why it uses the mouse position

Browser UI selectors change frequently. Using the current pointer location is intentionally simple and avoids hard-coded coordinates or brittle browser automation. The deliberate hover also prevents accidental capture submission to the wrong app.

## Privacy and safety

The bridge captures the entire left half of the primary display. Close or move notifications, passwords, private messages, and other sensitive material before pressing F8.

Captured frames are stored in `bridge_captures/` by default for debugging. Set `save_captures=False` in `BridgeConfig` if they should not be retained.

## Optional automatic submission

In `ethan_bridge.py`, change:

```python
BridgeConfig(auto_submit=False)
```

to:

```python
BridgeConfig(auto_submit=True)
```

Manual submission is strongly recommended for the first tests.

## Current limitations

- Windows-first because image clipboard support uses `pywin32`.
- Captures only the primary monitor.
- This is push-to-look, not continuous autonomous viewing.
- ChatGPT still needs a user message for each reaction.
