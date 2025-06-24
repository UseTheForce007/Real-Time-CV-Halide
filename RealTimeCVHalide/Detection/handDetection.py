import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,  # Use tracking for video
    max_num_hands=2,
    min_detection_confidence=0.5,
)
drawing_utils = mp.solutions.drawing_utils


def classify_gesture(landmarks):
    """
    Classify hand gesture based on landmarks.

    Parameters:
    landmarks (list): List of (x, y, z) tuples for hand landmarks.

    Returns:
    str: Detected gesture.
    """
    # Check for first finger gesture (index finger extended)
    if landmarks[8][1] < landmarks[6][1] and landmarks[12][1] > landmarks[10][1]:
        return "First Finger"

    # Check for two fingers gesture (index and middle fingers extended)
    if (
        landmarks[8][1] < landmarks[6][1]
        and landmarks[12][1] < landmarks[10][1]
        and landmarks[16][1] > landmarks[14][1]
    ):
        return "Two Fingers"

    # Check for closed fist gesture (all fingers curled)
    if all(landmarks[i][1] > landmarks[i - 2][1] for i in [4, 8, 12, 16, 20]):
        return "Closed Fist"

    # Check for open hand gesture (all fingers extended)
    if all(landmarks[i][1] < landmarks[i - 2][1] for i in [4, 8, 12, 16, 20]):
        return "Open Hand"

    return "Unknown Gesture"


def detect_hands(image):
    """
    Detect hands in an image using MediaPipe Hands.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).

    Returns:
    tuple: Processed image with landmarks drawn, and a list of detected hand information.
    """

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    hand_info = []  # To store hand landmarks, handedness, and gestures

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Draw landmarks on the image
            drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            # Get handedness (left or right hand)
            handedness = results.multi_handedness[idx].classification[0].label

            # Extract landmarks
            landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]

            # Classify gesture
            gesture = classify_gesture(landmarks)

            # Append hand info
            hand_info.append(
                {
                    "handedness": handedness,
                    "landmarks": landmarks,
                    "gesture": gesture,
                }
            )

    return image, hand_info
