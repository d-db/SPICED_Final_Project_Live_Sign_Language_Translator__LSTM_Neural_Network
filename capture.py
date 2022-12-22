"""
Script to record sign language signs that can later be used to train the LSTM neural network.
Before entering the for loop to save the sign, the script will once record a video of the sign and save
it at the defined location in a folder called "video".
In the current configuration the script will perform 200 iterations of 30 frames each to record the sign.
For each frame the sign will be saved as numpy arrays containing the x,y and z values of the defined landmarks
using the MediaPipe-library by Google.
The script will automatically create a folder structure with 200 folder numbered from 0 to 199.
After running through the script each folder will contain 30 numpy arrays - one for each frame.

Example call of the script through the terminal for the sign "brauchen" whose files should be
saved at "./data/":
> python3 script.py brauchen ./data/
"""
import sys
import cv2 as cv2
import os
import numpy as np
import mediapipe as mp
import pyshine as ps
from capture_functions import mediapipe_detection, draw_styled_landmarks, extract_keypoints, capture_video

# Suppress unnecessary Tensorflow messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if __name__ == "__main__":

    mp_holistic = mp.solutions.holistic  # Holistic model
    mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

    # Set global variables
    ACTION = sys.argv[1]
    DATA_PATH = os.path.join(str(sys.argv[2]))
    # The script will perform 200
    NO_SEQUENCES = 200
    LENGTH_SEQUENCES = 30

    # Create folders for every frame
    for sequence in range(NO_SEQUENCES):
        try:
            os.makedirs(os.path.join(DATA_PATH, ACTION, str(sequence)))
        except:
            sys.exit("Folder already exists.")

    # Create a folder for the Video
    os.makedirs(os.path.join(DATA_PATH, ACTION, "Video"))

    # Set MediaPipe model
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        path = os.path.join(DATA_PATH, ACTION, "Video")

        cap = capture_video(ACTION, path, holistic, 4)

        for sequence in range(NO_SEQUENCES):
            for frame_num in range(LENGTH_SEQUENCES):
                # Read feed
                ret, frame = cap.read()

                # Make detections
                image, results = mediapipe_detection(frame, holistic)

                # Draw landmarks
                draw_styled_landmarks(image, results)

                # At frame 0 inform the user that a new iteration is starting
                # and wait for 0.5 seconds so that he/she cann prepare for executing the sign
                if frame_num == 0:
                    ps.putBText(image, 'BEGINN DER AUFNAHME', text_offset_x=300, text_offset_y=300, vspace=10,
                                hspace=10, font_scale=2.0,
                                background_RGB=(255, 255, 255), text_RGB=(0, 0, 0))
                    # Show on top of the screen the the name of the sign
                    # and the number of signs performed so far
                    cv2.putText(image, 'Aufnahme Gebaerde "{}" - Video Nummer {} von {}'.format(ACTION, sequence,
                                                                                                NO_SEQUENCES),
                                (15, 27),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('Gebaerden Aufnahme', image)
                    cv2.moveWindow('Gebaerden Aufnahme', 80, 50)
                    cv2.waitKey(500)
                else:
                    cv2.putText(image, 'Aufnahme Gebaerde "{}" - Video Nummer {} von {}'.format(ACTION, sequence,
                                                                                                NO_SEQUENCES),
                                (15, 27),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    # Show to screen
                    cv2.imshow('Gebaerden Aufnahme', image)
                    cv2.moveWindow('Gebaerden Aufnahme', 80, 50)

                # Export landmarks of each frame and save them as numpy array
                keypoints = extract_keypoints(results)
                npy_path = os.path.join(DATA_PATH, ACTION, str(sequence), str(frame_num))
                np.save(npy_path, keypoints)

                # Break gracefully
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    sys.exit("...")

        cap.release()
        cv2.destroyAllWindows()
