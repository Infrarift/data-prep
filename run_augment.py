import os
import cv2
import numpy as np

from augment.noise import PoissonNoise
from visualization.image_strip import ImageStrip

K_INPUT_DIR = "input"

if __name__ == "__main__":
    print("Run Augment")
    image_list = os.listdir(K_INPUT_DIR)
    for file_name in image_list:
        file_path = os.path.join(K_INPUT_DIR, file_name)
        image = cv2.imread(file_path)

        p_noise = PoissonNoise()
        image2 = p_noise.augment_gaussian(image)

        images = [image, image2]
        image_strip = ImageStrip()
        image_out = image_strip.produce(images)

        cv2.imshow("Image", image_out)
        key = cv2.waitKey()
        key = chr(key)
        print(image)
