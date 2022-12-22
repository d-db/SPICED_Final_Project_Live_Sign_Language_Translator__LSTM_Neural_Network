# SPICED_Final_Project_Live_Sign_Language_Translator

## Project Summary

main.py performs a live translation of the German sign language and displays the translated word directly in the window. In the assumed use case, an appointment should be made possible between a deaf and a hearing person. The LSTM neural network is trained to identify 16 different signs of the German sign language. If the user executes the German sign for "stop", a 'speech-to-text' translator will be started. If the user executes the german sign for "end", the programm will end.

The project has been realised within two weeks and all training data has been solely produced by the author of this project.

## Demonstration Video

https://user-images.githubusercontent.com/61935581/209193653-3dc91bb2-fecc-4960-8581-1e963a9e5aaf.mp4

The English translation of the video content and more details:

- Part 1 (in sign language): "Good morning, I need an appointment."
(This is followed by the German sign for "Stop", which automatically starts a speech-to-text GUI).

- Part 2 (speech-to-text): "Hello, we have something free on Tuesday at 4pm. If that suits you, please tell me your name. Thank you very much."
(At this point I have shortened the video by about 7 seconds to speed up the process in the video a bit).

- Part 3 (in sign language): "Thank you my name is Daniel"
(Then follows the German sign for "end", which ends the whole application)

## Acknowledgement

Many thanks to Nicholas Renotte and [his amazing video about 'action recognition' with Googles MediaPipe library](https://www.youtube.com/watch?v=doDUihpj6ro). Without this important inspiration, the project would not have been possible in this form.

## Installation

Clone the repository and create a new virtual environment

```bash
python3 -m venv envname # to create the virtual env
source envname/bin/activate # activate it
```

Afterwards install the libraries specified in requirements.txt

```bash
pip install -r requirements.txt
```

