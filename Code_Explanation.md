The main script "drowsiness_detection.py" does the following:

Initializes the video capture from the webcam.
Loads the pre-trained Dlib face detector and facial landmark predictor.
Defines a function to calculate the eye aspect ratio (EAR).
In a loop, captures frames from the webcam and processes each frame to detect faces and facial landmarks.
Calculates the EAR for both eyes and checks if it is below a certain threshold for a specified amount of time.
If drowsiness is detected, displays warning messages on the screen.
