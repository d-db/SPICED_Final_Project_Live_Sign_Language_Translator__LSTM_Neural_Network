"""
This project is inspired by Nicholas Renotte. Please check his amazing YouTube channel!
Main file of the 'German Sign Language Live Translator' that connects the 'sign language translator'
and the 'speech-to-text' translator in one while-loop.
The LSTM neural network at its core is trained to recognise 16 different vocabularies (static and dynamic).
Each sign has been recorded between 500 and 700 times using the capture.py script.
The use case was an appointment with a hairdresser, where a short dialogue
between a hearing and a deaf person should be made possible (check README.md for a demonstration video).
"""
import translate
from translate import capture_sign_language
from speech_to_text import window

if __name__ == "__main__":

    while True:

        # Run sign language translator
        capture_sign_language()

        # Break while loop if "end" sign is detected through the sign language translator
        if translate.break_process:
            break
        # Switch to "speech-to-text" translator if "stop" sign is detected through the sign language translator
        if translate.open_translator:
            window()
            translate.open_translator = False
            translate.active = True