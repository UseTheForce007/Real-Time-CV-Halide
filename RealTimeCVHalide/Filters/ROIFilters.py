import cv2


def generate_roi_with_filter(image, landmarks, margin=20, filter_function=None):
    """
    Generate an ROI around the fingertips of the right hand and apply a filter.

    Parameters:
    image (numpy.ndarray): Input image in BGR format (H, W, 3).
    landmarks (list): List of (x, y, z) tuples for hand landmarks.
    margin (int): Margin around the fingertip for the ROI.
    filter_function (callable): Function to apply a filter to the ROI.

    Returns:
    numpy.ndarray: Image with filtered ROIs.
    """
    height, width, _ = image.shape

    # Define the indices for the fingertips
    fingertip_indices = [8, 12]  # Thumb, Index, Middle, Ring, Pinky

    for idx in fingertip_indices:
        x = int(landmarks[idx][0] * width)
        y = int(landmarks[idx][1] * height)

        # Define the ROI rectangle
        top_left = (max(0, x - margin), max(0, y - margin))
        bottom_right = (min(width, x + margin), min(height, y + margin))

        # Extract the ROI
        roi = image[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]]

        # Apply the filter to the ROI if a filter function is provided
        if filter_function and roi.size > 0:
            filtered_roi = filter_function(roi)
            if len(filtered_roi.shape) == 2:  # Grayscale image
                filtered_roi = cv2.cvtColor(filtered_roi, cv2.COLOR_GRAY2BGR)

            # Replace the filtered ROI back into the original image
            image[top_left[1] : bottom_right[1], top_left[0] : bottom_right[0]] = (
                filtered_roi
            )

    return image
