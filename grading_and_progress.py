import tkinter as tk
from tkinter.ttk import Progressbar
import threading


class App(threading.Thread):
    """
    A class for tracking progress and displaying a progress bar.

    Args:
        window_title (str): The title of the progress bar window.
        window_size (str): The size of the progress bar window.
        progress_length (int): The length of the progress bar.
        progress_mode (str): The mode of the progress bar.

    Attributes:
        window (tk.Tk): The progress bar window.
        progress_bar (Progressbar): The progress bar widget.
        progress_value (int): The current progress value.

    """

    def __init__(self, window_title, window_size, progress_length, progress_mode):
        self.window_title = window_title
        self.window_size = window_size
        self.progress_length = progress_length
        self.progress_mode = progress_mode

        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.window.quit()

    def run(self):
        self.window = tk.Tk()

        # Set the window title and dimensions
        self.window.title(self.window_title)
        self.window.geometry(self.window_size)

        # Create a progress bar widget
        self.progress_bar = Progressbar(
            self.window, orient=tk.HORIZONTAL, length=self.progress_length, mode=self.progress_mode)

        # Set the initial progress value to 0
        self.progress_value = 0
        self.progress_bar['value'] = self.progress_value

        # Create a button to trigger the progress update
        self.update_button = tk.Button(
            self.window, text="Update Progress", command=self.update_progress)

        # Pack the progress bar and button widgets into the window
        self.progress_bar.pack(pady=20)
        self.update_button.pack(pady=10)

        self.window.mainloop()

    # Define a function that updates the progress value by 10 and calls the progress bar widget's update method
    def update_progress(self):
        self.progress_value += 3
        self.progress_bar['value'] = self.progress_value
        self.progress_bar.update()

    def is_done(self):
        return self.progress_value >= 100
