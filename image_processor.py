import cv2  # for image processing
import random  # for random values
import numpy as np  # for array operations


class Alteration:
    def apply(self, image, x, y, w, h):
        pass  # base class, nothing here just for structure


class ColourShift(Alteration):
    def apply(self, image, x, y, w, h):
        # taking region from image
        region = image[y:y+h, x:x+w].astype(np.int16)  # convert to int16 to avoid overflow

        # shifting colours slightly
        region[:, :, 0] = np.clip(region[:, :, 0] + 30, 0, 255)  # red channel
        region[:, :, 1] = np.clip(region[:, :, 1] + 15, 0, 255)  # green channel
        region[:, :, 2] = np.clip(region[:, :, 2] + 20, 0, 255)  # blue channel

        # putting back to image
        image[y:y+h, x:x+w] = region.astype(np.uint8)
        

class BlurEffect(Alteration):
    def apply(self, image, x, y, w, h):
        region = image[y:y+h, x:x+w]  # select region
        # apply gaussian blur on that part
        image[y:y+h, x:x+w] = cv2.GaussianBlur(region, (15, 15), 0)


class BrightnessChange(Alteration):
    def apply(self, image, x, y, w, h):
        # changing brightness and contrast slightly
        image[y:y+h, x:x+w] = cv2.convertScaleAbs(image[y:y+h, x:x+w], alpha=1.2, beta=35)


class ImageProcessor:
    def __init__(self):
        # list of all possible alterations
        self.alterations = [ColourShift(), BlurEffect(), BrightnessChange()]

    def process_image(self, file_path):
        original = cv2.imread(file_path)  # read image from file

        if original is None:  # if not loaded properly
            raise ValueError("Image could not be loaded.")

        # convert BGR to RGB (opencv uses BGR by default)
        original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
        original = cv2.resize(original, (450, 300))  # resize image

        modified = original.copy()  # copy image to apply changes
        difference_regions = []  # store diff areas

        # create 5 differences
        for _ in range(5):
            x, y, w, h = self.create_non_overlapping_region(difference_regions)  # get safe region

            alteration = random.choice(self.alterations)  # pick random effect
            alteration.apply(modified, x, y, w, h)  # apply effect

            difference_regions.append((x, y, w, h))  # save region

        return original, modified, difference_regions  # return all

    def create_non_overlapping_region(self, existing_regions):
        while True:  # keep trying until valid region found
            w = random.randint(35, 60)  # random width
            h = random.randint(35, 60)  # random height

            x = random.randint(10, 450 - w - 10)  # random x within bounds
            y = random.randint(10, 300 - h - 10)  # random y within bounds

            new_region = (x, y, w, h)  # create region tuple

            # check overlap
            if not self.is_overlapping(new_region, existing_regions):
                return new_region  # return if valid

    def is_overlapping(self, new_region, existing_regions):
        x1, y1, w1, h1 = new_region  # unpack new region

        # check with all existing ones
        for x2, y2, w2, h2 in existing_regions:
            # logic to check overlapping rectangles
            if not (x1 + w1 < x2 or x1 > x2 + w2 or y1 + h1 < y2 or y1 > y2 + h2):
                return True  # overlap found

        return False  # no overlap