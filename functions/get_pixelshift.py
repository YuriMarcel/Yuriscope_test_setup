import cv2
import numpy as np
from PIL import Image
import time

def compute_shift(image_path1, image_path2):
    # Load BMP images and convert to grayscale

    start_time = time.time()
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    # Define the motion model
    warp_mode = cv2.MOTION_TRANSLATION

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv2.MOTION_HOMOGRAPHY:
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else:
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Specify the number of iterations and termination criteria
    number_of_iterations = 5000
    termination_eps = 1e-10
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)

    # Run the ECC algorithm to compute the warp matrix
    _, warp_matrix = cv2.findTransformECC(img2, img1, warp_matrix, warp_mode, criteria)

    # Extract the translation from the warp matrix
    dx = warp_matrix[0,2]
    dy = warp_matrix[1,2]

    
    total_time = time.time() - start_time
    print(f"Total time needed: {round(total_time,1)}s")
    return dx, dy

paths = [
    ("/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3101.bmp", "/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3102.bmp"),
    ("/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3102.bmp", "/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3103.bmp"),
    ("/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3103.bmp", "/home/rm/Desktop/Yuriscope_pictures/NEMUCO_cells_2/pictures/LED_3104.bmp")
]

# Pixelversatz für jedes Bildpaar berechnen
shifts = [compute_shift(p1, p2) for p1, p2 in paths]

# Durchschnittswerte berechnen
avg_dx = sum([s[0] for s in shifts]) / len(shifts)
avg_dy = sum([s[1] for s in shifts]) / len(shifts)

print(f"Durchschnittlicher Pixelversatz in x-Richtung: {avg_dx}")
print(f"Durchschnittlicher Pixelversatz in y-Richtung: {avg_dy}")
