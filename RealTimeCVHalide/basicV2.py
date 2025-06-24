from Filters.ROIFilters import generate_roi_with_filter
from Filters.filters import blur_filter, greyscale_filter, pixelate_filter
from Detection.handDetection import detect_hands
import cv2

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
    hand_detected_frame, hand_info = detect_hands(frame)

    if not hand_info:
        continue

    # Initialize the filter to None
    selected_filter = None

    # Determine the filter based on the left hand's gesture
    for hand in hand_info:
        if hand["handedness"] == "Left":
            gesture = hand["gesture"]
            print(f"Detected Gesture: {gesture} for Left Hand")

            if gesture == "First Finger":
                selected_filter = greyscale_filter
            elif gesture == "Two Fingers":
                selected_filter = blur_filter
            elif gesture == "Open Hand":
                selected_filter = pixelate_filter

    # Apply the selected filter to the right hand's ROIs
    for hand in hand_info:
        if hand["handedness"] == "Right" and selected_filter:
            frame = generate_roi_with_filter(
                frame, hand["landmarks"], margin=20, filter_function=selected_filter
            )

    # Display the processed frame
    cv2.imshow("Feed", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
