import numpy as np


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
