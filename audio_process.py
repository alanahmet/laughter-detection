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
        self.stream = sd.Stream(callback=self.audio_level)
        self.stream.start()

    def audio_level(self, indata, outdata, frames, time, status):
        """
        A method to check the sound level.

        Args:
        indata (numpy.ndarray): An array of audio samples.
        outdata (numpy.ndarray): An array of audio samples.
        frames (int): The number of frames.
        time (CData): A ctypes structure containing timing information.
        status (CallbackFlags): A callback status object.
        """
        rms = np.sqrt(np.mean(indata**2))
        # Print loud if the rms is above a threshold (0.2)
        if rms > 0.2:
            self.loud = True
        else:
            self.loud = False

    def is_loud(self):
        return self.loud


if __name__ == "__main__":
    tester = ListenSound()
