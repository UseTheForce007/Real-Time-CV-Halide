import cv2
from Filters import greyscale, blur


# Open the default webcam (0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame.")
        break
    # Convert the frame to greyscale using the naive filter
    grey_frame = greyscale.greyscale_naive(frame)
    # Apply blur filter to the frame
    blurred_frame = blur.blur_naive(frame, kernel_size=5)

    # Display the original frame and the greyscale frame and blurred frame
    cv2.imshow("Original Webcam Feed", frame)
    # cv2.imshow("Greyscale Webcam Feed", grey_frame)
    cv2.imshow("Blurred Webcam Feed", blurred_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
