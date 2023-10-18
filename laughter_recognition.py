import numpy as np
import speech_recognition as sr


class LaughterRecognizer:
    """
    A class for recognizing laughter sounds using a microphone and Google Speech Recognition API.

    Attributes:
        audio_threshold (int): The maximum amplitude of the audio signal required to detect laughter sounds.
        recognizer (speech_recognition.Recognizer): The speech recognition engine used to recognize speech.
        microphone (speech_recognition.Microphone): The microphone used to capture audio.

    Methods:
        recognize_laughter_sound(): Captures a short audio segment from the microphone and recognizes laughter sounds.
    """

    def __init__(self, audio_threshold=5000):
        self.audio_threshold = audio_threshold
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def recognize_laughter_sound(self):
        # Adjust the microphone sensitivity to ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

        # Capture a short audio segment from the microphone
        try:
            audio = self.recognizer.listen(
                source, timeout=1, phrase_time_limit=1)
        except sr.WaitTimeoutError:
            # If no audio is captured, return False
            return False

        # Convert the audio segment to a numpy array
        audio_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)

        # Compute the maximum amplitude of the audio signal
        max_amplitude = np.max(np.abs(audio_data))

        # Check if the maximum amplitude is above the threshold
        if max_amplitude > self.audio_threshold:
            # Try to recognize the audio segment using Google Speech Recognition API
            try:
                transcript = self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                # If no speech is recognized, return False
                return False

            # Check if the transcript contains the word "laugh" or "haha"
            if "laugh" in transcript.lower() or "haha" in transcript.lower():
                # Return True if laughter sound is detected
                return True

        # Return False otherwise
        return False
