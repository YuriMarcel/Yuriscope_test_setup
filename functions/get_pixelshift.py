import numpy as np
import imageio
import matplotlib.pyplot as plt

def pixelshift(img1_path, img2_path):
    # Bilder mit imageio laden
    image1 = imageio.imread(img1_path, as_gray=True)
    image2 = imageio.imread(img2_path, as_gray=True)

    # Diskrete schnelle Fourier-Transformation und komplexe Konjugation von image2
    image1FFT = np.fft.fft2(image1)
    image2FFT = np.conjugate(np.fft.fft2(image2))

    # Inverse Fourier-Transformation des Produkts -> entspricht der Kreuzkorrelation
    imageCCor = np.real(np.fft.ifft2(image1FFT * image2FFT))

    # Verschieben Sie die Nullfrequenzkomponente in die Mitte des Spektrums
    imageCCorShift = np.fft.fftshift(imageCCor)

    # Bestimmen Sie die Entfernung des Maximums vom Zentrum
    row, col = image1.shape
    yShift, xShift = np.unravel_index(np.argmax(imageCCorShift), (row, col))
    yShift -= int(row / 2)
    xShift -= int(col / 2)

    # Ergebnisse anzeigen
    plt.figure()
    plt.imshow(image1, cmap='gray')
    plt.title('Image 1')

    plt.figure()
    plt.imshow(image2, cmap='gray')
    plt.title('Image 2')

    plt.figure()
    plt.imshow(imageCCorShift, cmap='hot')
    plt.title('Cross-Correlation')
    plt.colorbar()

    plt.show()

    print("Versatz in x-Richtung [Pixel]:", xShift)
    print("Versatz in y-Richtung [Pixel]:", yShift)

    return xShift, yShift

# Beispielaufruf
x_shift, y_shift = pixelshift('path_to_image1.bmp', 'path_to_image2.bmp')
