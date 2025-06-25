import os

os.environ["LIBGL_DEBUG"] = "quiet"

import cv2
from Filters import greyscale, blur, pixelate
from Detection import handDetection
import timeit


# Open the default webcam (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Detect hands and get handedness, landmarks, and gestures
    hand_detected_frame, hand_info = handDetection.detect_hands(frame)

    if not hand_info:
        continue
    elif hand_info:
        # Apply filters based on detected hand gestures
        for hand in hand_info:
            if hand["handedness"] == "Left":  # Process only the left hand
                gesture = hand["gesture"]
                print(f"Detected Gesture: {gesture} for Left Hand")

                if gesture == "First Finger":
                    frame = greyscale.greyscale_bgr_cv(frame)
                elif gesture == "Two Fingers":
                    frame = blur.blur_bgr_cv(frame)
                elif gesture == "Open Hand":
                    frame = pixelate.pixelate_cv2(frame)

        cv2.imshow("Feed", frame)

    # # Display detected hand information
    # for hand in hand_info:
    #     print(f"Hand: {hand['handedness']}")
    #     print(f"Gesture: {hand['gesture']}")
    #     # print(f"Landmarks: {hand['landmarks']}")

    # Display the original frame and the hand detection frame
    # cv2.imshow("Original Webcam Feed", frame)
    # cv2.imshow("Hand Detection Webcam Feed", hand_detected_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
