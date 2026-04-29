import tkinter as tk  # for GUI
from tkinter import filedialog, messagebox  # for file open dialog and popup messages
from PIL import Image, ImageTk  # for handling the images

from image_processor import ImageProcessor  # custom file for processing image
from game_logic import GameLogic  # custom file for game logic

class GUIApp:
    def __init__(self):
        self.root = tk.Tk()  # creating main window
        self.root.title("Spot the Difference Game")  # setting title

        self.processor = ImageProcessor()  # object for processing images
        self.logic = None  # game logic will be assigned later

        self.original_photo = None  # store original image
        self.modified_photo = None  # store modified image

        self.left_x = 50  # x position for left image
        self.right_x = 550  # x position for right image
        self.image_y = 120  # y position for both images

        self.create_widgets()  # calling function to create UI
