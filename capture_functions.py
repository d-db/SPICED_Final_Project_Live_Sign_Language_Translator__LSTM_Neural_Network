import cv2 as cv2
import numpy as np
import mediapipe as mp
import time

mp_holistic = mp.solutions.holistic  # Holistic model
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities


def capture_video(action, path, holistic, length):
    """
    Function to record and save a video.
    It is used within capture.py before the iterations to save the landmarks begin.
    Returns the 'video' variable
    """
    video = cv2.VideoCapture(0)
    frame_width = int(video.get(3))
    frame_height = int(video.get(4))

    size = (frame_width, frame_height)

    start_time = int(time.time())

    result = cv2.VideoWriter(path + f'/video_{action}.avi',
                             cv2.VideoWriter_fourcc(*'MJPG'),
                             10, size)

    while True:
        ret, frame = video.read()

        if ret:
            # Make detections
            image, results = mediapipe_detection(frame, holistic)

            # Draw landmarks
            draw_styled_landmarks(image, results)

            # Write the frame into the
            # file 'filename.avi'
            result.write(image)

            # Put a text on the screen in order to inform the user
            cv2.putText(image, f"Einmalige Video Aufnahme - Laenge: {length} Sekunden",
                        (15, 27), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the frame
            # saved in the file
            cv2.imshow('Aufnahme Video', image)
            cv2.moveWindow('Aufnahme Video', 80, 50)

            # Press S on keyboard
            # to stop the process
            if cv2.waitKey(1) & 0xFF == ord('s'):
                break

            if int(time.time()) - start_time > length:
                break

            # Break the loop
        else:
            break

    result.release()
    cv2.destroyAllWindows()

    return video


def mediapipe_detection(image, model):
    """
    Convert color scheme and apply the MediaPipe model on the frame
    Return the image and the results
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False  # Image is no longer writeable
    results = model.process(image)  # Make prediction
    image.flags.writeable = True  # Image is now writeable
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # COLOR COVERSION RGB 2 BGR
    return image, results


def draw_landmarks(image, results):
    """
    Draw the extracted landmarks from 'result' on 'image'
    """
    mp_drawing.draw_landmarks(image, results.pose_landmarks,
                              mp_holistic.POSE_CONNECTIONS)  # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks,
                              mp_holistic.HAND_CONNECTIONS)  # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks,
                              mp_holistic.HAND_CONNECTIONS)  # Draw right hand connections


def draw_styled_landmarks(image, results):
    """
    Adjust the style of the drawn landmarks
    """
    # # Draw face connections
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION,
    #                           mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
    #                           mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
    #                           )
    # # Draw face connections
    # mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS,
    #                           mp_drawing.DrawingSpec(color=(80, 110, 10), thickness=1, circle_radius=1),
    #                           mp_drawing.DrawingSpec(color=(80, 256, 121), thickness=1, circle_radius=1)
    #                           )
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(80, 22, 10), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(80, 44, 121), thickness=2, circle_radius=2)
                              )
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(121, 44, 250), thickness=2, circle_radius=2)
                              )
    # Draw right hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS,
                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                              )


def extract_keypoints(results):
    """
    Convert the extracted landmarks to a numpy array.
    If no hand movements are detected, create a numpy array in the right shape consisting of zeros.
    Return the numpy array and 'counter', which indicated if any hand movement has been recognized
    """
    counter = 0

    # Use only the first 22 pose landmarks that represent the upper body
    pose = np.array([[res.x, res.y] for res in results.pose_landmarks.landmark[:23]]).flatten() \
        if results.pose_landmarks else np.zeros(23*2)
    # face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() \
    #     if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() \
        if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() \
        if results.right_hand_landmarks else np.zeros(21*3)
    # If no movement of the right hand is detected, increase 'counter' by 1
    if np.all((rh == 0)):
        counter += 1
    array = np.concatenate([pose, lh, rh])
    return array, counter