import numpy as np
import cv2


def greyscale_naive(image):
    """
    Convert an image to greyscale using a naive approach.

    Parameters:
    image (numpy.ndarray): Input` image in RGB format (H, W, 3).

    Returns:
    numpy.ndarray: Greyscale image (H, W).
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel RGB image.")

    # Calculate the greyscale value using the luminosity method
    grey_image = np.dot(image[..., :3], [0.299, 0.587, 0.114])

    return grey_image.astype(np.uint8)


def greyscale_bgr_cv(image):
    """
    Convert an image to greyscale using OpenCV's BGR to Grayscale conversion.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).

    Returns:
    numpy.ndarray: Greyscale image (H, W).
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel BGR image.")

    grey_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    return grey_image
