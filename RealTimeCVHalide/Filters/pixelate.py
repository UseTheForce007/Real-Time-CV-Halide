import cv2
import numpy as np


def pixelate_cv2(image, pixel_size=10):
    """
    Pixelate an image by reducing its resolution and then resizing it back to the original size.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).
    pixel_size (int): Size of the pixelation block.

    Returns:
    numpy.ndarray: Pixelated image (H, W, 3).
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel BGR image.")

    # Resize the image to a smaller size
    small_image = cv2.resize(
        image,
        (image.shape[1] // pixel_size, image.shape[0] // pixel_size),
        interpolation=cv2.INTER_LINEAR,
    )

    # Resize it back to the original size
    pixelated_image = cv2.resize(
        small_image, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST
    )

    return pixelated_image
