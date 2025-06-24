import numpy as np


def blur_naive(image, kernel_size=5):
    """
    Apply a naive blur filter to an image.

    Parameters:
    image (numpy.ndarray): Input image in RGB format (H, W, 3).
    kernel_size (int): Size of the blur kernel (must be odd).

    Returns:
    numpy.ndarray: Blurred image (H, W, 3).
    """
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel RGB image.")

    if kernel_size % 2 == 0:
        raise ValueError("Kernel size must be an odd integer.")

    pad_size = kernel_size // 2
    padded_image = np.pad(
        image, ((pad_size, pad_size), (pad_size, pad_size), (0, 0)), mode="edge"
    )

    blurred_image = np.zeros_like(image)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            blurred_image[i, j] = np.mean(
                padded_image[i : i + kernel_size, j : j + kernel_size], axis=(0, 1)
            )

    return blurred_image.astype(np.uint8)
