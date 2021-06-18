import cv2
import numpy as np
from PIL import ImageEnhance

FILTER_NAMES = {
    'Original': 'original',
    'Grayscale': 'grayscale',
    'Desenho': 'sketch',
    'Sépia': 'sepia',
    'Blur': 'blur',
    'Canny': 'canny',
    'Contraste': 'contrast',
    'Brilho': 'brightness'
}

OUTPUT_WIDTH = 500


class Filters:
    def __init__(self, st, original_image):
        self.st = st
        self.original_image = original_image
        self.selected_filter = st.sidebar.radio("Filtros", [key for key in FILTER_NAMES.keys()])

    def __call__(self, width=OUTPUT_WIDTH):
        run = getattr(self, FILTER_NAMES.get(self.selected_filter))
        result_image = run()
        self.st.image(result_image, width=width)

    def grayscale(self):
        converted_image = np.array(self.original_image)
        gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
        return gray_image

    def sketch(self):
        converted_image = np.array(self.original_image)
        gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
        inv_gray_image = 255 - gray_image
        blur_image = cv2.GaussianBlur(inv_gray_image, (21, 21), 0, 0)
        sketch_image = cv2.divide(gray_image, 255 - blur_image, scale=256)
        return sketch_image

    def sepia(self):
        converted_image = np.array(self.original_image)
        converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
        kernel = np.array([[0.272, 0.534, 0.132],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia_image = cv2.filter2D(converted_image, -1, kernel)
        sepia_image = cv2.cvtColor(sepia_image, cv2.COLOR_BGR2RGB)
        return sepia_image

    def blur(self):
        b_amount = self.st.sidebar.slider("Kernel (n x n)", 3, 81, 9, step=2)
        converted_image = np.array(self.original_image)
        converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
        blur_image = cv2.GaussianBlur(converted_image, (b_amount, b_amount), 0, 0)
        blur_image = cv2.cvtColor(blur_image, cv2.COLOR_BGR2RGB)
        return blur_image

    def canny(self):
        threshold1 = self.st.sidebar.slider("Limite inferior", 50, 300, 100, step=10)
        threshold2 = self.st.sidebar.slider("Limite superior", 100, 300, 150, step=10)
        converted_image = np.array(self.original_image)
        converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
        blur_image = cv2.GaussianBlur(converted_image, (11, 11), 0)
        canny_image = cv2.Canny(blur_image, threshold1, threshold2)
        return canny_image

    def contrast(self):
        c_amount = self.st.sidebar.slider("Contraste", 0.01, 2.0, 1.0)
        enhancer = ImageEnhance.Contrast(self.original_image)
        contrast_image = enhancer.enhance(c_amount)
        return contrast_image

    def brightness(self):
        b_amount = self.st.sidebar.slider("Brilho", 0.01, 2.0, 1.0)
        enhancer = ImageEnhance.Brightness(self.original_image)
        brightness_image = enhancer.enhance(b_amount)
        return brightness_image

    def original(self):
        return self.original_image
