"""
Ethan Watch-Party Bridge

A no-API bridge between a video playing on the left half of the screen and an
open ChatGPT conversation on the right.

Workflow:
1. Put the video on the left and this ChatGPT conversation on the right.
2. Hover the mouse over the ChatGPT message composer.
3. Press F8.
4. The bridge captures the left half, copies it as an image, clicks the composer,
   pastes the image, and types a short reaction request.
5. Review it and press Enter yourself.

Windows-first because copying images to the clipboard is handled with pywin32.
"""

from __future__ import annotations

import io
import os
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import keyboard
import pyautogui
from PIL import ImageGrab

try:
    import win32clipboard
except ImportError as exc:  # pragma: no cover - platform/dependency guard
    raise SystemExit(
        "pywin32 is required on Windows. Install dependencies with: "
        "pip install -r requirements.txt"
    ) from exc


DEFAULT_PROMPT = (
    "React to what we're watching together. Don't narrate the obvious. "
    "Notice the subtext, absurdity, scamminess, awkwardness, or whatever is "
    "actually funny or interesting. Talk directly to me as Ethan: warm, dry, "
    "playful, concise, and on my side. If the image is unclear, say so instead "
    "of inventing details."
)


@dataclass(frozen=True)
class BridgeConfig:
    hotkey: str = "f8"
    capture_side: str = "left"
    paste_delay_seconds: float = 0.8
    type_interval_seconds: float = 0.002
    auto_submit: bool = False
    save_captures: bool = True


class EthanBridge:
    def __init__(self, config: BridgeConfig | None = None) -> None:
        self.config = config or BridgeConfig()
        self._busy = threading.Lock()
        self.capture_dir = Path(__file__).with_name("bridge_captures")
        if self.config.save_captures:
            self.capture_dir.mkdir(exist_ok=True)

    def capture_video_region(self):
        """Capture one half of the primary display."""
        screen_width, screen_height = pyautogui.size()
        half = screen_width // 2

        if self.config.capture_side.lower() == "right":
            bbox = (half, 0, screen_width, screen_height)
        else:
            bbox = (0, 0, half, screen_height)

        image = ImageGrab.grab(bbox=bbox, all_screens=False)

        if self.config.save_captures:
            stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image.save(self.capture_dir / f"watch_{stamp}.png")

        return image

    @staticmethod
    def copy_image_to_clipboard(image) -> None:
        """Copy a PIL image to the Windows clipboard as DIB data."""
        with io.BytesIO() as output:
            image.convert("RGB").save(output, "BMP")
            dib_data = output.getvalue()[14:]  # Strip BMP file header.

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dib_data)
        finally:
            win32clipboard.CloseClipboard()

    def send_glance(self) -> None:
        """Capture, paste, and compose one deliberate watch-party glance."""
        if not self._busy.acquire(blocking=False):
            print("A glance is already being prepared.")
            return

        try:
            print("Capturing the video side...")
            image = self.capture_video_region()
            self.copy_image_to_clipboard(image)

            # The user deliberately hovers over the ChatGPT composer before F8.
            # Clicking the current pointer location avoids brittle browser selectors.
            pyautogui.click()
            time.sleep(self.config.paste_delay_seconds)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(self.config.paste_delay_seconds)

            # Add a newline after the image before typing the instruction.
            pyautogui.hotkey("shift", "enter")
            pyautogui.write(
                DEFAULT_PROMPT,
                interval=self.config.type_interval_seconds,
            )

            if self.config.auto_submit:
                time.sleep(0.25)
                pyautogui.press("enter")
                print("Sent to ChatGPT.")
            else:
                print("Ready in ChatGPT. Review it, then press Enter to send.")

        except Exception as exc:
            print(f"Bridge error: {exc}", file=sys.stderr)
        finally:
            self._busy.release()

    def run(self) -> None:
        print("=" * 64)
        print("ETHAN WATCH-PARTY BRIDGE")
        print("=" * 64)
        print("Video on the left. ChatGPT on the right.")
        print("Hover over the ChatGPT message box and press F8.")
        print("Press Ctrl+Shift+Q to quit.")
        print()

        keyboard.add_hotkey(
            self.config.hotkey,
            lambda: threading.Thread(target=self.send_glance, daemon=True).start(),
        )
        keyboard.wait("ctrl+shift+q")


if __name__ == "__main__":
    EthanBridge().run()
