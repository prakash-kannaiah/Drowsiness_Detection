# Drowsiness Detection

This project implements a drowsiness detection system using Python, OpenCV, and Dlib. The system detects the drowsiness of a driver by monitoring their eye aspect ratio (EAR) and displays a warning message on the screen when drowsiness is detected.

## Features

- Real-time drowsiness detection using a webcam.
- Uses Dlib's pre-trained facial landmark predictor.
- Calculates the eye aspect ratio to detect drowsiness.
- Displays warning messages on the screen when drowsiness is detected.

## Requirements

- Python 3.x
- OpenCV
- Dlib
- Scipy

## Installation

1. Clone this repository to your local machine:

    ```bash
    https://github.com/prakash-kannaiah/Drowsiness_Detection.git
    cd drowsiness-detection
    ```

2. Create and activate a new Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Download the facial landmark predictor model and place it in the `shape` directory:

    - [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)

5. Extract the `.bz2` file:

    ```bash
    bzip2 -d shape/shape_predictor_68_face_landmarks.dat.bz2
    ```

## Project Structure

drowsiness-detection/
- shape/
-- shape_predictor_68_face_landmarks.dat
- drowsiness_detection.py
- requirements.txt
- README.md
- LICENSE

## Usage

Run the drowsiness detection script:

```bash
python drowsiness_detection.py
