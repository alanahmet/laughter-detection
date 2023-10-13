import sounddevice as sd
import numpy as np
import threading
import tkinter as tk


class ListenSound(threading.Thread):
    """
    A class to handle sound testing.

    Attributes:
    stream (sd.Stream): A stream object to capture audio from microphone.
    """

    def __init__(self):
        """
        Initializes the ListenSound object and starts the stream.
        """
        threading.Thread.__init__(self)
        self.stream = sd.Stream(callback=self.is_loud)
        self.stream.start()

    def is_loud(self, indata, outdata, frames, time, status):
        """
        A method to check the sound level.

        Args:
        indata (numpy.ndarray): An array of audio samples.
        outdata (numpy.ndarray): An array of audio samples.
        frames (int): The number of frames.
        time (CData): A ctypes structure containing timing information.
        status (CallbackFlags): A callback status object.
        """
        global is_loud
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > 1:
            is_loud = True
        else:
            is_loud = False


if __name__ == "__main__":
    tester = ListenSound()
