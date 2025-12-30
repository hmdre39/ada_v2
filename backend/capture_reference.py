"""
Capture Reference Image for Face Authentication
Run this script to take a photo of yourself for face unlock
"""
import cv2
import platform
import os

print("=" * 60)
print("JARVIS Face Authentication - Reference Photo Capture")
print("=" * 60)
print()
print("Instructions:")
print("1. Look directly at the camera")
print("2. Make sure you're well-lit (no shadows on face)")
print("3. Press SPACE to capture your reference photo")
print("4. Press ESC to cancel")
print()

# Open camera with correct API for Windows
if platform.system() == 'Windows':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
elif platform.system() == 'Darwin':
    cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)
else:
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Could not open camera!")
    print("Please check:")
    print("  - Camera is connected")
    print("  - Camera permissions are granted")
    print("  - No other app is using the camera")
    input("\nPress Enter to exit...")
    exit(1)

print("Camera opened successfully!")
print("Waiting for you to capture reference photo...\n")

while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Failed to read frame from camera")
        break
    
    # Display instructions on frame
    cv2.putText(frame, "Press SPACE to capture, ESC to cancel", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.putText(frame, "Look directly at camera", 
                (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    cv2.imshow('Capture Reference Photo', frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == 32:  # SPACE key
        # Save the reference image
        output_path = os.path.join(os.path.dirname(__file__), "reference.jpg")
        cv2.imwrite(output_path, frame)
        print(f"\n✓ Reference photo saved to: {output_path}")
        print(f"  Image size: {frame.shape[1]}x{frame.shape[0]} pixels")
        print("\nYou can now close this window and restart JARVIS.")
        print("Face authentication will now work!")
        
        # Show saved image for confirmation
        cv2.putText(frame, "SAVED! Close this window", 
                    (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 
                    1.0, (0, 255, 0), 2)
        cv2.imshow('Capture Reference Photo', frame)
        cv2.waitKey(2000)  # Show for 2 seconds
        break
        
    elif key == 27:  # ESC key
        print("\nCapture cancelled.")
        break

cap.release()
cv2.destroyAllWindows()
print("\nDone!")
