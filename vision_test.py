"""
Quick test to verify llava vision model
"""
import ollama
import pyautogui
from datetime import datetime

print("Testing llava vision model...")
print("\n1. Taking a screenshot...")

# Take a test screenshot
screenshot = pyautogui.screenshot()
test_file = f"test_vision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
screenshot.save(test_file)
print(f"   Screenshot saved: {test_file}")

print("\n2. Sending to llava model...")
try:
    response = ollama.chat(
        model="llava:7b",
        messages=[{
            'role': 'user',
            'content': 'What do you see in this image? Describe it in one sentence.',
            'images': [test_file]
        }]
    )
    
    result = response['message']['content']
    print(f"\n3. Model response:\n   {result}")
    
    # Check if it's actually seeing the image
    if "language model" in result.lower() or "cannot see" in result.lower() or "can't see" in result.lower():
        print("\n❌ PROBLEM: Model is not processing the image!")
        print("   The model is giving a default 'I can't see' response.")
        print("\n   Try these fixes:")
        print("   1. Reinstall llava: ollama pull llava:7b")
        print("   2. Try llava:13b instead: ollama pull llava:13b")
        print("   3. Check ollama is updated: ollama --version")
    else:
        print("\n✅ SUCCESS: Vision model is working!")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\n   Make sure you have:")
    print("   1. Ollama installed and running")
    print("   2. llava model downloaded: ollama pull llava:7b")