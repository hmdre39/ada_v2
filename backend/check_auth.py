"""
Diagnostic script to check face authentication setup
"""
import os
import cv2
import platform

print("=" * 60)
print("JARVIS Face Authentication - Diagnostic Check")
print("=" * 60)
print()

# Check 1: Reference image exists
ref_path = os.path.join(os.path.dirname(__file__), "reference.jpg")
print(f"1. Checking reference image: {ref_path}")
if os.path.exists(ref_path):
    print("   ✓ File exists")
    img = cv2.imread(ref_path)
    if img is not None:
        print(f"   ✓ Image readable: {img.shape[1]}x{img.shape[0]} pixels")
    else:
        print("   ✗ File exists but cannot be read (corrupted?)")
else:
    print("   ✗ File NOT found")
    print("   → Run 'python capture_reference.py' to create it")

print()

# Check 2: MediaPipe model
model_path = os.path.join(os.path.dirname(__file__), "face_landmarker.task")
print(f"2. Checking MediaPipe model: {model_path}")
if os.path.exists(model_path):
    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    print(f"   ✓ Model exists ({size_mb:.1f} MB)")
else:
    print("   ✗ Model NOT found")
    print("   → Will auto-download on first run")

print()

# Check 3: Camera access
print(f"3. Checking camera access (Platform: {platform.system()})")
try:
    if platform.system() == 'Windows':
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    elif platform.system() == 'Darwin':
        cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
    else:
        cap = cv2.VideoCapture(0)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print(f"   ✓ Camera working ({frame.shape[1]}x{frame.shape[0]})")
        else:
            print("   ✗ Camera opened but cannot read frames")
        cap.release()
    else:
        print("   ✗ Cannot open camera")
        print("   → Check camera permissions and connections")
except Exception as e:
    print(f"   ✗ Camera error: {e}")

print()

# Check 4: Settings
settings_path = os.path.join(os.path.dirname(__file__), "settings.json")
print(f"4. Checking settings: {settings_path}")
if os.path.exists(settings_path):
    import json
    with open(settings_path, 'r') as f:
        settings = json.load(f)
    face_auth = settings.get('face_auth_enabled', False)
    if face_auth:
        print("   ✓ Face authentication ENABLED")
    else:
        print("   ✗ Face authentication DISABLED")
        print("   → Set 'face_auth_enabled': true in settings.json")
else:
    print("   ✗ Settings file not found")

print()
print("=" * 60)
print("Summary:")
if os.path.exists(ref_path):
    print("  Everything looks good! If still not working:")
    print("  1. Check server logs for detailed error messages")
    print("  2. Make sure lighting is good (no shadows on face)")
    print("  3. Try recreating reference: python capture_reference.py")
else:
    print("  ACTION REQUIRED: Create reference image")
    print("  → Run: python capture_reference.py")
print("=" * 60)
