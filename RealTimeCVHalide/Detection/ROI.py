import cv2


def generate_roi(image, landmarks, margin=20):
    """
    Generate an ROI around the fingertips of the right hand.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).
    landmarks (list): List of (x, y, z) tuples for hand landmarks.
    margin (int): Margin around the fingertip for the ROI.

    Returns:
    numpy.ndarray: Image with ROI drawn around the fingertips.
    """
    height, width, _ = image.shape

    # Define the indices for the fingertips
    fingertip_indices = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky

    for idx in fingertip_indices:
        x = int(landmarks[idx][0] * width)
        y = int(landmarks[idx][1] * height)

        # Define the ROI rectangle
        top_left = (x - margin, y - margin)
        bottom_right = (x + margin, y + margin)

        # Draw the ROI on the image
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)

    return image
