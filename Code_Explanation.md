**Code Explanation**

The main script `drowsiness_detection.py` is designed to detect driver drowsiness in real-time using a webcam feed. It leverages the Dlib library for face and landmark detection and OpenCV for image processing and display. Here's a step-by-step breakdown of what the script does:

**Initialization**

**1. Video Capture Initialization**
   
   cap = cv2.VideoCapture(0)
   - The script initializes video capture from the webcam.

**2. Loading Dlib Models**
   
   face_detector = dlib.get_frontal_face_detector()
   dlib_facelandmark = dlib.shape_predictor("shape/shape_predictor_68_face_landmarks.dat")
   - Loads the pre-trained Dlib face detector and facial landmark predictor.

**Functions**

**3. Eye Aspect Ratio Calculation**
   
   def detect_eye_aspect_ratio(eye_points):
       poi_A = distance.euclidean(eye_points[1], eye_points[5])
       poi_B = distance.euclidean(eye_points[2], eye_points[4])
       poi_C = distance.euclidean(eye_points[0], eye_points[3])
       aspect_ratio = (poi_A + poi_B) / (2 * poi_C)
       return aspect_ratio
   - Defines a function to calculate the Eye Aspect Ratio (EAR), which helps in detecting whether the eyes are closed.

**Constants**

**4. Thresholds**
   
   EAR_THRESHOLD = 0.250
   TIME_THRESHOLD = 3
   - Sets the EAR threshold and the time threshold for detecting drowsiness.

**Main Loop**

**5. Frame Capture and Processing**
   
   while True:
       ret, frame = cap.read()
       if not ret:
           break
       gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       faces = face_detector(gray_scale)
   - Captures frames from the webcam and converts them to grayscale for face detection.

**6. Face and Landmark Detection**
   
   for face in faces:
       x, y, w, h = face.left(), face.top(), face.width(), face.height()
       cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
       face_landmarks = dlib_facelandmark(gray_scale, face)
   - Detects faces in the frame and draws rectangles around them.
   - Detects facial landmarks within the detected faces.

**7. Eye Landmark Extraction and EAR Calculation**
   
   left_eye_points = [(face_landmarks.part(n).x, face_landmarks.part(n).y) for n in range(36, 42)]
   right_eye_points = [(face_landmarks.part(n).x, face_landmarks.part(n).y) for n in range(42, 48)]
   left_eye_ratio = detect_eye_aspect_ratio(left_eye_points)
   right_eye_ratio = detect_eye_aspect_ratio(right_eye_points)
   average_eye_ratio = (left_eye_ratio + right_eye_ratio) / 2
   - Extracts eye landmarks and calculates the EAR for both eyes.

**8. Drowsiness Detection**
   
   if average_eye_ratio < EAR_THRESHOLD:
       if start_time is None:
           start_time = time.time()
       drowsy_time = time.time() - start_time
       if drowsy_time > TIME_THRESHOLD:
           cv2.rectangle(frame, (45, 70), (475, 130), (255, 255, 255), -1)
           cv2.rectangle(frame, (45, 420), (475, 480), (255, 255, 255), -1)
           cv2.putText(frame, "DROWSINESS DETECTED", (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 210), 3)
           cv2.putText(frame, "Braking!!! ", (50, 450), cv2.FONT_HERSHEY_PLAIN, 2, (21, 56, 212), 3)
   else:
       start_time = None
       drowsy_time = 0
   - Checks if the average EAR is below the threshold. If so, it starts a timer.
   - If the eyes remain closed for longer than the time threshold, it displays warning messages on the screen.

**Display and Termination**

**9. Display and Break Condition**
   
   cv2.imshow("Drowsiness Detection", frame)
   if cv2.waitKey(10) & 0xFF == ord('q'):
       break
   - Displays the processed frame and allows the user to break the loop by pressing the 'q' key.

**10. Resource Release**
    
    cap.release()
    cv2.destroyAllWindows()
    - Releases the webcam and closes all OpenCV windows when the loop ends.

This script effectively detects drowsiness by monitoring the eye aspect ratio and provides real-time feedback by displaying warning messages when drowsiness is detected.
