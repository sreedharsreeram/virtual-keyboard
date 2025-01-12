# OpenCV - Virtual Keyboard

## Why

I've been interested in getting into computer vision, so I created this project to gain a basic understanding of the libraries used and to practice Python. My main goal is to work on more meaningful projects that can be useful in the real world.

## What it does

This script uses the MediaPipe hand tracking model to detect hand movements through the webcam. MediaPipe is a machine learning pipeline that tracks the position of your hand in real-time. When your finger hovers over a key, it simulates a keypress, allowing you to type hands-free. It’s an intuitive way to interact with the virtual keyboard, making it easy and fun to type without using your hands on word/notepad or any text editor!


## Tech Stack
- Python
- MediaPipe Hands:  A hand landmark ML model that operates on the cropped image region defined by the palm detector and returns high-fidelity 3D hand keypoints.
- OpenCV: For video processing and rendering the keyboard interface.
- cvzone: For hand-tracking and gesture recognition.
- Pynput: For simulating keyboard inputs.
- NumPy: For efficient numerical operations in image processing.

You can test it out right now!
Clone the repository:
```sh
git clone https://github.com/sreedharsreeram/virtual-keyboard
```
Install the required dependencies:
```sh
pip install -r requirements.txt
```
Run the code:
```sh
python main.py
```

