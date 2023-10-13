import speech_recognition as sr
import librosa
import numpy as np

# Initialize the speech recognition recognizer
recognizer = sr.Recognizer()

# Start capturing audio from the microphone
microphone = sr.Microphone()

# Set the laughter detection threshold
laughter_threshold = 0.5

# Initialize variables for continuous laughter detection
laughter_duration = 0
# Maximum duration for continuous laughter (in seconds)
max_laughter_duration = 10

while True:
    # Capture audio from the microphone
    with microphone as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        # Recognize speech from the captured audio
        text = recognizer.recognize_google(audio)

        # Convert the audio to a numpy array for audio analysis
        audio_np = np.array(audio.get_array_of_samples())

        # Compute the audio energy using librosa
        energy = np.sum(audio_np ** 2)

        # Check if the audio energy exceeds the laughter threshold
        if energy > laughter_threshold:
            # Perform further processing for continuous laughter detection
            laughter_duration += audio.duration
            if laughter_duration >= max_laughter_duration:
                # Generate the reward QR code# ...
                print("laughter detected")

        # Print the recognized speech and audio energy
        print(f"Recognized Speech: {text}")
        print(f"Audio Energy: {energy}")

    except sr.UnknownValueError:
        print("Could not understand the audio.")


# Break the loop if the 'q' key is pressed
    if input("Press 'q' to quit.") == 'q':
        break
