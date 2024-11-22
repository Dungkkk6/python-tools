import cv2
import numpy as np
from skimage.filters import threshold_otsu
from skimage.color import rgb2gray
from scipy.ndimage.filters import gaussian_filter

def photo_to_manga(input_image, output_image):
    # Load the image
    img = cv2.imread(input_image)

    # Convert to grayscale
    gray = rgb2gray(img)

    # Apply Gaussian blur
    blurred = gaussian_filter(gray, sigma=1)

    # Perform Otsu's thresholding
    thresh = threshold_otsu(blurred)
    binary = (blurred > thresh).astype(float)

    # Invert the image
    binary = 1 - binary

    # Apply dilation and erosion to enhance the edges
    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # Convert the image back to RGB
    manga_image = np.stack([eroded, eroded, eroded], axis=-1)

    # Save the output image
    cv2.imwrite(output_image, (manga_image * 255).astype(np.uint8))

if __name__ == "__main__":
    photo_to_manga("input_photo.jpg", "output_manga.jpg")