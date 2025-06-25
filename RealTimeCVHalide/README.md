# Real-Time Computer Vision with Hand Gesture Filters

This project implements a real-time computer vision application using OpenCV and MediaPipe. It captures video from the webcam, detects hand gestures, and applies filters to specific regions of interest (ROIs) based on the detected gestures. The application also includes an FPS counter to display the frame rate on the video feed.

## Features

1. **Hand Gesture Detection**: Detects hand gestures using MediaPipe.
2. **Filter Application**: Applies filters (grayscale, blur, pixelate) to ROIs based on gestures.
3. **FPS Counter**: Displays the frame rate on the video feed.
4. **Index Finger ROI**: Ensures compatibility with index finger-based ROI generation.
5. **Modular Design**: Refactored code for modularity and maintainability.

## Journey So Far

1. Added functionality to detect hand gestures using MediaPipe.
2. Implemented filters (grayscale, blur, pixelate) that can be applied based on gestures.
3. Refactored code to modularize ROI-based filter addition and application.
4. Integrated an FPS counter to monitor the frame rate.
5. Ensured compatibility with index finger-based ROI generation.

## File Overview

### `basicV2.py`

This is the main script that:
- Captures video from the webcam.
- Detects hand gestures.
- Applies filters to ROIs based on gestures.
- Displays the processed video feed with an FPS counter.

#### Functions

1. **`add_filters_based_on_rois`**
   - **Description**: Adds the selected filter and ROI to the active filters list.
   - **Parameters**:
     - `hand` (dict): Information about the detected hand.
     - `frame` (numpy.ndarray): The current video frame.
     - `selected_filter` (callable): The filter function to apply.
     - `active_filters` (list): List to store active filters and their ROIs.
   - **Details**: Identifies the index finger's position, calculates an ROI around it, and appends the filter and ROI to the active filters list.

2. **`apply_active_filters`**
   - **Description**: Applies all active filters to the frame.
   - **Parameters**:
     - `frame` (numpy.ndarray): The current video frame.
     - `active_filters` (list): List of active filters and their ROIs.
   - **Returns**: The processed video frame.
   - **Details**: Iterates through the active filters list, applies each filter to its corresponding ROI, and updates the frame.

#### Main Loop

1. Captures frames from the webcam.
2. Detects hands and their gestures.
3. Selects filters based on left-hand gestures.
4. Adds filters to ROIs based on the right hand's index finger.
5. Applies all active filters to the frame.
6. Displays the processed frame with an FPS counter.
7. Exits on pressing the 'q' key.

## Usage

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Run the script using `python basicV2.py`.
4. Use gestures with the left hand to select filters and the right hand to apply them to specific regions.

## Dependencies

- Python 3.7+
- OpenCV
- MediaPipe

## Future Enhancements

1. Add support for more gestures and filters.
2. Optimize performance for higher FPS.
3. Extend functionality to support multiple hands and dynamic gestures.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
