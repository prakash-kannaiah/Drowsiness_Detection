# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 11:37:21 2024

@author: prakash kannaiah_edutech
"""

import cv2
import dlib
from scipy.spatial import distance
import time

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Load the pre-trained dlib face detector
face_detector = dlib.get_frontal_face_detector()

# Load the facial landmark predictor
dlib_facelandmark = dlib.shape_predictor("shape/shape_predictor_68_face_landmarks.dat")

def detect_eye_aspect_ratio(eye_points):
    """Calculate the aspect ratio for the eye."""
    poi_A = distance.euclidean(eye_points[1], eye_points[5])
    poi_B = distance.euclidean(eye_points[2], eye_points[4])
    poi_C = distance.euclidean(eye_points[0], eye_points[3])
    aspect_ratio = (poi_A + poi_B) / (2 * poi_C)
    return aspect_ratio

# Threshold for the Eye Aspect Ratio
EAR_THRESHOLD = 0.250
# Time threshold in seconds
TIME_THRESHOLD = 3

# Variables to keep track of time
start_time = None
drowsy_time = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the grayscale frame
    faces = face_detector(gray_scale)

    for face in faces:
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # Detect facial landmarks
        face_landmarks = dlib_facelandmark(gray_scale, face)
        
        # Draw points for all facial landmarks
        for n in range(68):
            x_point = face_landmarks.part(n).x
            y_point = face_landmarks.part(n).y
            cv2.circle(frame, (x_point, y_point), 1, (0, 255, 0), -1)
        
        # Extract eye landmarks
        left_eye_points = [(face_landmarks.part(n).x, face_landmarks.part(n).y) for n in range(36, 42)]
        right_eye_points = [(face_landmarks.part(n).x, face_landmarks.part(n).y) for n in range(42, 48)]
        
        # Draw lines connecting the landmarks for the left eye
        for i in range(36, 42):
            next_point = 36 if i == 41 else i + 1
            cv2.line(frame, (face_landmarks.part(i).x, face_landmarks.part(i).y), 
                     (face_landmarks.part(next_point).x, face_landmarks.part(next_point).y), 
                     (0, 255, 0), 1)
        
        # Draw lines connecting the landmarks for the right eye
        for i in range(42, 48):
            next_point = 42 if i == 47 else i + 1
            cv2.line(frame, (face_landmarks.part(i).x, face_landmarks.part(i).y), 
                     (face_landmarks.part(next_point).x, face_landmarks.part(next_point).y), 
                     (0, 255, 0), 1)
        
        # Calculate the eye aspect ratios
        left_eye_ratio = detect_eye_aspect_ratio(left_eye_points)
        right_eye_ratio = detect_eye_aspect_ratio(right_eye_points)
        average_eye_ratio = (left_eye_ratio + right_eye_ratio) / 2
        
        # Check for drowsiness
        if average_eye_ratio < EAR_THRESHOLD:
            if start_time is None:
                start_time = time.time()
            drowsy_time = time.time() - start_time
            
            if drowsy_time > TIME_THRESHOLD:
                # Draw white boxes for the text
                cv2.rectangle(frame, (45, 70), (475, 130), (255, 255, 255), -1)
                cv2.rectangle(frame, (45, 420), (475, 480), (255, 255, 255), -1)
                # Display drowsiness detected text
                cv2.putText(frame, "DROWSINESS DETECTED", (50, 100), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 210), 3)
                cv2.putText(frame, "Braking!!! ", (50, 450), 
                            cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 212), 3)
        else:
            start_time = None
            drowsy_time = 0
    
    # Display the resulting frame
    cv2.imshow("Drowsiness Detection", frame)
    
    # Break the loop on 'q' key press
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
