import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,  # Use tracking for video
    max_num_hands=2,
    min_detection_confidence=0.5,
)
drawing_utils = mp.solutions.drawing_utils


def detect_hands(image):
    """
    Detect hands in an image using MediaPipe Hands.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).

    Returns:
    numpy.ndarray: Image with hand landmarks drawn.
    """

    # Optionally resize for speed (e.g., 50% smaller)
    # small = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)
    # rgb_image = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    # curent time hand detection time: 0.0256 seconds

    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            drawing_utils.draw_landmarks(
                image, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

    return image
