import argparse
import cv2
import qrcode
import tensorflow as tf
from deepface import DeepFace

import audio_process as ap
import grading_and_progress as gp


class FacialDetection:
    def __init__(self, source_id):
        # Check the number of available GPUs
        print("Num GPUs Available: ", len(
            tf.config.list_physical_devices('GPU')))

        # Create a progress bar
        self.grading = gp.App("Laughter Grading System",
                              "600x50", 550, 'determinate')

        # Load the pre-trained face detection cascade
        self.face_cascade = cv2.CascadeClassifier(
            './model/haarcascade_frontalface_default.xml')

        # Load the pre-trained emotion recognition model
        self.emotion_model = DeepFace.build_model("Emotion")

        if source_id == "0":
            source_id = 0

        # Start capturing video from the source
        self.video_capture = cv2.VideoCapture(source_id)

        # Initialize variables
        self.is_done = False
        self.sound_info = ap.ListenSound()

    def detect_faces(self):
        while not self.is_done:
            # Read each frame from the video capture
            ret, frame = self.video_capture.read()

            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the grayscale frame
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Perform emotion recognition on each detected face
            for (x, y, w, h) in faces:
                face = frame[y:y+h, x:x+w]
                is_emotion_detected = True
                try:
                    emotions = DeepFace.analyze(face, actions=['emotion'])
                except:
                    is_emotion_detected = False
                if is_emotion_detected == True:
                    emotion = emotions[0]

                # Check if the dominant emotion is happy and the sound level is loud
                if emotion['dominant_emotion'] == 'happy':  # and self.sound_info.is_loud()
                    # Perform continuous laughter detection

                    print("laughter detected")
                    self.grading.update_progress()

                    if self.grading.is_done():
                        # Generate QR code with a unique reward
                        reward = "https://your-reward-url.com"
                        qr = qrcode.QRCode(version=1, box_size=10, border=5)
                        qr.add_data(reward)
                        qr.make(fit=True)

                        # Save the QR code as an image file
                        qr_image = qr.make_image(
                            fill_color="black", back_color="white")
                        qr_image.save("reward_qr_code.png")
                        self.is_done = True
                        self.grading.callback()
                        break

            # Display the video capture with face detection
            cv2.imshow('Video', frame)

            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the video capture and close all windows
        self.video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Facial detection and emotion recognition')
    parser.add_argument('--source', type=str, default="0",
                        help='source video path, 0 for webcam (default: 0)')
    args = parser.parse_args()

    # Create a FacialDetection object and start detecting faces
    fd = FacialDetection(args.source)
    fd.detect_faces()


# import cv2
# from deepface import DeepFace
# import tensorflow as tf
# import grading_and_progress as gp
# import audio_process as ap
# import qrcode


# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
# grading = gp.App("Laughter Grading System", "600x50", 550, 'determinate')

# # Load the pre-trained face detection cascade
# face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')

# # Load the pre-trained emotion recognition model
# emotion_model = DeepFace.build_model("Emotion")

# # Start capturing video from the source
# video_capture = cv2.VideoCapture(0)

# is_done = False
# sound_info = ap.ListenSound()

# while not is_done:

#     # Read each frame from the video capture
#     ret, frame = video_capture.read()

# # Convert the frame to grayscale for face detection
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# # Detect faces in the grayscale frame
#     faces = face_cascade.detectMultiScale(
#         gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

# # For each detected face, perform emotion recognition
#     for (x, y, w, h) in faces:
#         face = frame[y:y+h, x:x+w]
#         is_emotion_detected = True
#         try:
#             emotions = DeepFace.analyze(face, actions=['emotion'])
#         except:
#             is_emotion_detected = False
#         if is_emotion_detected == True:
#             emotion = emotions[0]

#         # Check if the detected emotion is laughter
#             if emotion['dominant_emotion'] == 'happy' and sound_info.is_loud():
#                 # Perform further processing for continuous laughter detection# ...
#                 print("laughter detected")

#                 grading.update_progress()

#                 if grading.is_done():
#                     # Generate QR code with a unique reward
#                     reward = "https://your-reward-url.com"
#                     qr = qrcode.QRCode(version=1, box_size=10, border=5)
#                     qr.add_data(reward)
#                     qr.make(fit=True)

#                     # Save the QR code as an image file
#                     qr_image = qr.make_image(
#                         fill_color="black", back_color="white")
#                     qr_image.save("reward_qr_code.png")
#                     is_done = True
#                     grading.callback()
#                     break

#         # Display the video frame with bounding boxes and emotion labels
#             cv2.imshow('Video', frame)

#     # Break the loop if the 'q' key is pressed
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         print("quitting")
#         # Release the video capture and close the windows
#         is_done = True
#         grading.callback()
#         break

# # Release the video capture and close the windows
# video_capture.release()
# cv2.destroyAllWindows()
