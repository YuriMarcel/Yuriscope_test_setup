import numpy as np
import cv2

def get_beam_center(vid):
    
    for _ in range(5):
        ret, frame = vid.read()

    if not ret:
        raise ValueError("Error capturing image from video source.")
    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rows_x, cols_y = gray_frame.shape
    x, y = np.meshgrid(np.arange(rows_x), np.arange(cols_y), indexing='ij')

    centroidX = np.sum(x * gray_frame) / np.sum(gray_frame)
    centroidY = np.sum(y * gray_frame) / np.sum(gray_frame)
    
    mean_value = np.mean(gray_frame)
    overexposed_pixels = np.sum(gray_frame > 200)
     # Print the results
    print(f"Image Dimensions: {rows_x} x {cols_y}")
    print(f"Beamcenter Coordinates: X = {centroidX:.2f}, Y = {centroidY:.2f}")
    print(f"Mean Value: {mean_value:.2f}")
    print(f"Overexposed Pixels: {overexposed_pixels}")

    return rows_x, cols_y, centroidX, centroidY, mean_value, overexposed_pixels, frame, x, y

