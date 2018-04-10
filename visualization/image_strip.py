import numpy as np
import cv2


class ImageStrip:
    def __init__(self):
        pass

    @staticmethod
    def _get_output_dimensions(num_images, width, height, pad):
        total_width = num_images * (width + pad) + pad
        total_height = height + pad * 2
        return total_width, total_height

    def produce(self, images, label="", pad=5, bg_color=(0, 0, 0), size=None):

        # Assert that all images are the same dimensions.
        if size is None:
            size = images[0].shape
        width = size[1]
        height = size[0]
        n_images = len(images)

        # Create the template image.
        total_width, total_height = self._get_output_dimensions(n_images, width, height, pad)
        output_image = np.zeros((total_height, total_width, 3), dtype=np.uint8)

        # Draw original image.
        for i in range(n_images):
            self._draw_in_position(output_image, images[i], i, width, height, pad)

        return output_image

    def _draw_in_position(self, base_image, image, index, width, height, pad):
        top = pad
        bot = pad + height
        left = pad + index * (pad + width)
        right = left + width
        add_image = cv2.resize(image, (width, height))
        base_image[top:bot, left:right] = add_image
