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

    def create_widgets(self):
        # title label at top
        title = tk.Label(
            self.root,
            text="Spot the Difference Game",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=10)  # adding space

        button_frame = tk.Frame(self.root)  # frame for buttons
        button_frame.pack()

        # load image button
        load_button = tk.Button(
            button_frame,
            text="Load Image",
            font=("Arial", 14),
            command=self.load_image  # calls load_image when clicked
        )
        load_button.grid(row=0, column=0, padx=10)

        # reveal button
        reveal_button = tk.Button(
            button_frame,
            text="Reveal",
            font=("Arial", 14),
            command=self.reveal_differences  # calls reveal function
        )
        reveal_button.grid(row=0, column=1, padx=10)

        # canvas where images will show
        self.canvas = tk.Canvas(self.root, width=1050, height=450, bg="white")
        self.canvas.pack(pady=10)

        # status label at bottom
        self.status_label = tk.Label(
            self.root,
            text="Load an image to start",
            font=("Arial", 16)
        )
        self.status_label.pack(pady=10)

        # bind mouse click event
        self.canvas.bind("<Button-1>", self.handle_click)

    def load_image(self):
        # open file dialog to choose image
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if not file_path:  # if user cancel
            return

        try:
            # processing image and getting original, modified and differences
            original, modified, difference_regions = self.processor.process_image(file_path)
        except Exception as error:
            messagebox.showerror("Error", str(error))  # show error if something wrong
            return

        self.logic = GameLogic(difference_regions)  # create game logic object

        self.canvas.delete("all")  # clear previous drawings

        # converting numpy array images to Tk format
        self.original_photo = ImageTk.PhotoImage(Image.fromarray(original))
        self.modified_photo = ImageTk.PhotoImage(Image.fromarray(modified))

        # text above original image
        self.canvas.create_text(
            self.left_x + 225,
            30,
            text="Original Image",
            font=("Arial", 14, "bold")
        )

        # text above modified image
        self.canvas.create_text(
            self.right_x + 225,
            30,
            text="Modified Image (Click to find differences)",
            font=("Arial", 14, "bold")
        )

        # display original image
        self.canvas.create_image(
            self.left_x,
            self.image_y,
            anchor="nw",
            image=self.original_photo
        )

        # display modified image
        self.canvas.create_image(
            self.right_x,
            self.image_y,
            anchor="nw",
            image=self.modified_photo
        )

    def handle_click(self, event):
        if self.logic is None:  # if no game started
            return

        if self.logic.game_over:  # if game already finished
            messagebox.showinfo("Game Over", "Please load a new image to play again.")
            return

        # check if click is inside modified image
        if not self.is_click_on_modified_image(event.x, event.y):
            return

        # convert screen coords to image coords
        image_x = event.x - self.right_x
        image_y = event.y - self.image_y

        result = self.logic.check_click(image_x, image_y)  # check if correct click

        # if correct or finished draw red circle
        if result == "correct" or result == "finished":
            self.draw_red_circle(event.x, event.y)

        if result == "wrong":
            messagebox.showinfo("Wrong Click", "That is not a difference.")

        elif result == "mistake_limit":
            messagebox.showwarning(
                "Game Over",
                "You made 3 mistakes. No more guesses allowed."
            )

        elif result == "finished":
            messagebox.showinfo(
                "Congratulations",
                "You found all 5 differences!"
            )

        self.update_status()  # update label

    def is_click_on_modified_image(self, x, y):
        # checking if click is inside right image area
        return (
            self.right_x <= x <= self.right_x + 450
            and self.image_y <= y <= self.image_y + 300
        )
    def draw_red_circle(self, x, y):
        # draw circle on modified image
        self.canvas.create_oval(
            x - 18,
            y - 18,
            x + 18,
            y + 18,
            outline="red",
            width=3
        )

        # calculate corresponding position on original image
        original_x = x - self.right_x + self.left_x
        original_y = y

        # draw same circle on original image
        self.canvas.create_oval(
            original_x - 18,
            original_y - 18,
            original_x + 18,
            original_y + 18,
            outline="red",
            width=3
        )

    def reveal_differences(self):
        if self.logic is None:  # if no game
            return

        unfound_regions = self.logic.get_unfound_regions()  # get remaining diff

        # loop through all and draw blue circles
        for x, y, w, h in unfound_regions:
            self.draw_blue_circle(x, y, w, h)

        self.logic.game_over = True  # end game

        messagebox.showinfo(
            "Reveal",
            "All remaining differences have been revealed. Load a new image to restart."
        )

        self.update_status()

    def draw_blue_circle(self, x, y, w, h):
        # get center of rectangle
        center_x = x + w // 2
        center_y = y + h // 2

        # positions for both images
        right_center_x = self.right_x + center_x
        screen_y = self.image_y + center_y

        left_center_x = self.left_x + center_x

        # draw on modified image
        self.canvas.create_oval(
            right_center_x - 25,
            screen_y - 25,
            right_center_x + 25,
            screen_y + 25,
            outline="blue",
            width=3
        )

        # draw on original image
        self.canvas.create_oval(
            left_center_x - 25,
            screen_y - 25,
            left_center_x + 25,
            screen_y + 25,
            outline="blue",
            width=3
        )

    def update_status(self):
        # update status label text
        if self.logic is None:
            self.status_label.config(text="Load an image to start")
        else:
            self.status_label.config(
                text=f"Remaining: {self.logic.remaining} | Mistakes: {self.logic.mistakes}/3"
            )

    def run(self):
        self.root.mainloop()  # start GUI loop

        self.update_status()  # update game status
