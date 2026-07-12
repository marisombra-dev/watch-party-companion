"""
Ethan Watch-Party Bridge

A no-API bridge between a video playing on the left half of the screen and an
open ChatGPT conversation on the right.

Workflow:
1. Put the video on the left and this ChatGPT conversation on the right.
2. Hover the mouse over the ChatGPT message composer.
3. Press F8.
4. The bridge captures the left half, pastes it into ChatGPT, types a short
   reaction request, and submits the message automatically.

Windows-first because copying images to the clipboard is handled with pywin32.
"""

from __future__ import annotations

import io
import struct
import sys
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
        "pywin32 is required on Windows. Install bridge dependencies with: "
        "pip install pyautogui pillow keyboard pywin32"
    ) from exc


DEFAULT_PROMPT = ("Watch with me as Ethan: warm, dry, playful, concise. "
                  "React, do not narrate. If unclear, say so.")


@dataclass(frozen=True)
class BridgeConfig:
    hotkey: str = "f8"
    capture_side: str = "left"
    paste_delay_seconds: float = 2.5
    type_interval_seconds: float = 0.002
    auto_submit: bool = True
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

        stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        capture_path = self.capture_dir / f"watch_{stamp}.png"
        image.save(capture_path)

        return image, capture_path

    @staticmethod
    def copy_image_to_clipboard(image) -> None:
        """Copy a PIL image to the Windows clipboard as DIB data."""
        with io.BytesIO() as output:
            image.convert("RGB").save(output, "BMP")
            dib_data = output.getvalue()[14:]

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dib_data)
        finally:
            win32clipboard.CloseClipboard()

    @staticmethod
    def copy_file_to_clipboard(path: Path) -> None:
        """Copy a real PNG file to the clipboard as a Windows file drop."""
        dropfiles = struct.pack("IiiII", 20, 0, 0, 0, 1)
        file_list = (str(path.resolve()) + "\0\0").encode("utf-16le")

        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(15, dropfiles + file_list)
        finally:
            win32clipboard.CloseClipboard()

    def send_glance(self) -> None:
        """Capture, paste, compose, and submit one watch-party glance."""
        if not self._busy.acquire(blocking=False):
            print("A glance is already being prepared.")
            return

        try:
            print("Capturing and sending the video side...")
            image, capture_path = self.capture_video_region()

            # Focus ChatGPT, then paste the saved PNG as a real file attachment.
            pyautogui.click()
            time.sleep(0.25)
            self.copy_file_to_clipboard(capture_path)
            time.sleep(0.25)
            pyautogui.hotkey("ctrl", "v")

            # Give ChatGPT time to upload the file before typing the prompt.
            time.sleep(4.0)
            pyautogui.hotkey("shift", "enter")
            pyautogui.write(
                DEFAULT_PROMPT,
                interval=self.config.type_interval_seconds,
            )

            if self.config.auto_submit:
                time.sleep(1.5)
                pyautogui.press("enter")
                print("Sent to ChatGPT.")
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
        print("F8 captures, pastes, and sends automatically.")
        print("Press Ctrl+Shift+Q to quit.")
        print()

        keyboard.add_hotkey(
            self.config.hotkey,
            lambda: threading.Thread(target=self.send_glance, daemon=True).start(),
            suppress=True,
            trigger_on_release=True,
        )
        keyboard.wait("ctrl+shift+q")


if __name__ == "__main__":
    EthanBridge().run()

