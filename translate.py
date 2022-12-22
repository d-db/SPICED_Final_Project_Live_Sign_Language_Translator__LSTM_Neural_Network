"""
Script of the 'sign language translator'. It loads the trained LSTM neural network in the beginning
and categorizes on this basis the performed signs. Signs are saved as numpy arrays that contain
x,y and z values of designated landmarks using the MediaPipe library from Google.
Categorized signs will be immediately display in the window above the user.
If no sign is performed the program will show the sentence 'Keine Gebaerde durchgefuehrt'
which translates to 'No sign has been performed'.
If the user performs the German sign for 'stop', the program will switch to a speech-to-text translator.
If the user performs the German sign for 'end', the program will end.
"""
import pickle
import time
import cv2 as cv2
import pyshine as ps

import numpy as np
import mediapipe as mp

import os

from tensorflow import keras
from capture_functions import mediapipe_detection, draw_styled_landmarks, extract_keypoints

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Use this global variables to control main.py
break_process = False
active = True
open_translator = False


def capture_sign_language():
    # Length of on iteration lasts 30 frames
    # The same length as in capture.py must be entered here.
    LENGTH_SEQUENCE = 30

    mp_holistic = mp.solutions.holistic  # Holistic model
    mp_drawing = mp.solutions.drawing_utils  # Drawing utilities

    # Load the latest LSTM neural network (created by the Jupyter notebook)
    model = keras.models.load_model("./files/1212_model")

    # Load the latest label_map_reverse.bin (created by the Jupyter notebook)
    with open('./files/label_map_reverse.bin', 'rb') as f:
        label_map_reverse = pickle.load(f)

    cap = cv2.VideoCapture(0)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)

    # Use this thext if no sign is performed
    text = "Keine Gebaerde durchgefuehrt"

    # This counter is used to recognize when the first sign of a letter is performed.
    # This letter should then be capitalized.
    alphabet_counter = 0

    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        global active
        while active:

            # Use the list to store the numpy arrays of the recorded live footage
            res = []
            # Increase this number of frames with no hands are recorded.
            # If this number equals 30 at the end of one iteration (==30 frames) no sign has been detected.
            counter_hands = 0

            for frame_num in range(LENGTH_SEQUENCE):
                ret, frame = cap.read()

                image, results = mediapipe_detection(frame, holistic)

                draw_styled_landmarks(image, results)

                # Add a text at frame 28 to inform the user that he/she should prepare for the next iteration.
                if frame_num > 27:
                    ps.putBText(image, 'Naechste Gebaerde', text_offset_x=350, text_offset_y=400, vspace=10,
                                hspace=10, font_scale=2.0,
                                background_RGB=(255, 255, 255), text_RGB=(0, 0, 0))

                # Extract the 'keypoints' (coordinates of the hand and pose landmarks) as numpy arrays
                # and add them to list 'res'.
                # 'Counter' indicates if a hand has been detected during the frame.
                # If not, increase 'counter_hands' by 1.
                keypoints, counter = extract_keypoints(results)
                res.append(keypoints)
                counter_hands += counter

                cv2.rectangle(image, (0, 0), (frame_width, 100), (245, 117, 16), -1)

                if frame_num == 29:
                    # Only if hand movements have been detected during one iteration
                    # continue with the categorization through the LSTM neural network
                    if counter_hands < 30:
                        # If no hand movement has been detected set 'text' to:
                        # 'No sign has been performed'
                        if text == "Keine Gebaerde durchgefuehrt":
                            text = ""
                        # Convert list 'res' to a numpy array and expand its dimension
                        # in order to adjust its shape to what is demanded by the LSTM neural network
                        picture = np.expand_dims(np.array(res), axis=0)
                        # Execute a prediction on the expanded
                        y_pred = model.predict(picture)
                        # Find the word with the highest predicted probability
                        # within the list of all vocabularies the model has been trained on
                        word = label_map_reverse[np.argmax(y_pred)]

                        # Only continue if the predicted probability is higher then 80%
                        if np.amax(y_pred) > 0.8:
                            # If the predicted word is "stop"
                            # set the global variables in such a manner that
                            # 'main.py' will stop the 'sign language translator' and
                            # instead start the 'speech-to-text' translator
                            if word == "Stop":
                                active = False
                                global open_translator
                                open_translator = True
                                break

                            # If the predicted word is "end"
                            # set the global variables in such a manner that
                            # the while-loop in 'main.py' will break
                            if word == "Ende":
                                active = False
                                global break_process
                                break_process = True
                                break

                            # Identify the first sign of a letter and capitalize it
                            # Add the letter to 'text'
                            if word in ["d", "a", "n", "i", "e", "l"]:
                                if alphabet_counter == 0:
                                    text += word.upper()
                                    alphabet_counter += 1
                                else:
                                    text += word

                            # Add the identified word to 'text'
                            else:
                                text += word + " "

                    else:
                        text = "Keine Gebaerde durchgefuehrt"

                    time.sleep(1)

                # Put 'text' on the screen
                if len(text) > 0 and text != "Keine Gebaerde durchgefuehrt":
                    cv2.putText(image, text, (100, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2, cv2.LINE_AA)

                if text == "Keine Gebaerde durchgefuehrt":
                    cv2.putText(image, text, (200, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.8, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow('Deep Learning Gebaerden Uebersetzer', image)

                cv2.moveWindow('Deep Learning Gebaerden Uebersetzer', 80, 50)

                # Break gracefullyq
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    active = False
                    break_process = True
                    break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    capture_sign_language()