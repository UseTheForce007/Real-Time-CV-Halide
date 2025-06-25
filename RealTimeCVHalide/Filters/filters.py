import cv2


def blur_filter(roi):
    return cv2.GaussianBlur(roi, (15, 15), 0)


def greyscale_filter(roi):
    return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


def pixelate_filter(roi):
    h, w = roi.shape[:2]
    if h < 10 or w < 10:
        print(f"Warning: ROI too small (width={w}, height={h}). Skipping...")
        return roi
    temp = cv2.resize(roi, (w // 10, h // 10), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
