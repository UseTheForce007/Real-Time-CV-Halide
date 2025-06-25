"""
Module: basicV2.py

This module implements a real-time computer vision application using OpenCV and MediaPipe. It captures video from the webcam, detects hand gestures, and applies filters to specific regions of interest (ROIs) based on the detected gestures. The module also includes an FPS counter to display the frame rate on the video feed.

Journey so far:
1. Added functionality to detect hand gestures using MediaPipe.
2. Implemented filters (grayscale, blur, pixelate) that can be applied based on gestures.
3. Refactored code to modularize ROI-based filter addition and application.
4. Integrated an FPS counter to monitor the frame rate.
5. Ensured compatibility with index finger-based ROI generation.

Functions:
- add_filters_based_on_rois: Adds filters to the active filters list based on the index finger's ROI.
- apply_active_filters: Applies all active filters to the video frame.

Usage:
Run the script to start the webcam feed. Use gestures with the left hand to select filters and the right hand to apply them to specific regions.
"""

from Filters.ROIFilters import generate_roi_with_filter
from Filters.filters import blur_filter, greyscale_filter, pixelate_filter
from Detection.handDetection import detect_hands
import cv2
import time

# Open the default webcam (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# List to store active filters and their ROIs
active_filters = []


def add_filters_based_on_rois(hand, frame, selected_filter, active_filters):
    """
    Add the selected filter and ROI to the active filters list.

    Parameters:
    hand (dict): Information about the detected hand.
    frame (numpy.ndarray): The current video frame.
    selected_filter (callable): The filter function to apply.
    active_filters (list): List to store active filters and their ROIs.

    This function identifies the index finger's position, calculates an ROI around it, and appends the filter and ROI to the active filters list.
    """
    for idx in [8]:  # Index finger only
        x = int(hand["landmarks"][idx][0] * frame.shape[1])
        y = int(hand["landmarks"][idx][1] * frame.shape[0])
        margin = 20
        top_left = (max(0, x - margin), max(0, y - margin))
        bottom_right = (
            min(frame.shape[1], x + margin),
            min(frame.shape[0], y + margin),
        )
        active_filters.append(
            {"filter": selected_filter, "roi": (top_left, bottom_right)}
        )


def apply_active_filters(frame, active_filters):
    """
    Apply all active filters to the frame.

    Parameters:
    frame (numpy.ndarray): The current video frame.
    active_filters (list): List of active filters and their ROIs.

    Returns:
    numpy.ndarray: The processed video frame.

    This function iterates through the active filters list, applies each filter to its corresponding ROI, and updates the frame.
    """
    for active_filter in active_filters:
        top_left, bottom_right = active_filter["roi"]
        roi = frame[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]
        if roi.size > 0:
            filtered_roi = active_filter["filter"](roi)
            if len(filtered_roi.shape) == 2:  # Grayscale image
                filtered_roi = cv2.cvtColor(filtered_roi, cv2.COLOR_GRAY2BGR)
            frame[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]] = (
                filtered_roi
            )
    return frame


# Initialize variables for FPS calculation
fps = 0
prev_time = time.time()

# Main loop
"""
Main loop:
1. Captures frames from the webcam.
2. Detects hands and their gestures.
3. Selects filters based on left-hand gestures.
4. Adds filters to ROIs based on the right hand's index finger.
5. Applies all active filters to the frame.
6. Displays the processed frame with an FPS counter.
7. Exits on pressing the 'q' key.
"""

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    # Display FPS on the frame
    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )

    # Detect hands and get handedness, landmarks, and gestures
    hand_detected_frame, hand_info = detect_hands(frame)

    # if not hand_info:
    # continue

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
            elif gesture == "Three Fingers":
                selected_filter = pixelate_filter
            elif gesture == "Open Hand":
                # Clear all active filters
                active_filters.clear()
                print("All filters removed!")

    # Add new filters based on the right hand's ROIs
    for hand in hand_info:
        if hand["handedness"] == "Right" and selected_filter:
            add_filters_based_on_rois(hand, frame, selected_filter, active_filters)

    # Apply all active filters
    frame = apply_active_filters(frame, active_filters)

    # Display the processed frame
    cv2.imshow("Feed", frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
