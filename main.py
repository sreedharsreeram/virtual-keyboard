import cv2
import cvzone
import numpy as np
from time import sleep
from cvzone.HandTrackingModule import HandDetector

# Height and width of the webcam
videocap = cv2.VideoCapture(0)
videocap.set(3, 1280)
videocap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

# Define keyboard layout
key = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]
]

inputText = ""
max_chars = 15
caps_lock = False  # Track the state of CAPS lock

# Class for button creation
class Buttons:
    def __init__(self, pos, text, size=[65, 65]):  # Default size for keys
        self.pos = pos
        self.size = size
        self.text = text

    def drawbutton(self, img, color=(0, 0, 0)):
        x, y = self.pos
        w, h = self.size
        # Use a semi-transparent color (with alpha blending) instead of solid fill
        overlay = img.copy()
        cv2.rectangle(overlay, self.pos, (x + w, y + h), color, cv2.FILLED)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)  # Apply transparency
        font_scale = 1.5 if self.text != "DEL" else 1.2  # Adjust font size for "DEL"
        cv2.putText(img, self.text, (x + 15, y + 50), cv2.FONT_ITALIC, font_scale, (255, 255, 255), 3)
        return img

# Create buttons for the keyboard layout
buttonSet = []
for row_index, row in enumerate(key):
    for col_index, letter in enumerate(row):
        button_pos = [80 * col_index + 15, 70 * row_index + 50]  # Adjusted spacing for keyboard
        button_size = [65, 65]  # Default size for buttons
        buttonSet.append(Buttons(button_pos, letter, button_size))

# Add space, caps lock, and delete keys below the keyboard (closer to the keyboard)
buttonSet.append(Buttons([20, 360], "DEL", [150, 65]))  # DEL button closer to the keyboard
buttonSet.append(Buttons([190, 360], "SPACE", [400, 65]))  # SPACE button closer to the keyboard
buttonSet.append(Buttons([600, 360], "CAPS", [150, 65]))  # CAPS button closer to the keyboard

key_pressed = False  # Track if a key was pressed

while True:
    success, img = videocap.read()
    hands, img = detector.findHands(img)
    length = None  # Initialize length to avoid undefined variable

    left_hand_detected = False  # Flag for left hand detection
    right_hand_detected = False  # Flag for right hand detection

    if hands:
        # Check if the right or left hand is detected
        for hand in hands:
            if hand["type"] == "Right":  # Only work if right hand is detected
                right_hand_detected = True
            if hand["type"] == "Left":  # Set flag if left hand is detected
                left_hand_detected = True

        if left_hand_detected:
            # Show message and hide everything else when left hand is detected
            cv2.putText(img, "Please use your right hand", (200, 50), cv2.FONT_ITALIC, 1.5, (0, 0, 255), 3)
            # Skip the rest of the loop, no keyboard or text box will be drawn
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            continue  # Skip the rest of the loop when left hand is detected

        if right_hand_detected:
            lmList = hands[0]["lmList"]  # Right hand's landmarks
            if lmList:
                x_tip, y_tip = lmList[8][:2]  # Index fingertip
                x_mid, y_mid = lmList[12][:2]  # Middle fingertip

                for button in buttonSet:
                    x, y = button.pos
                    w, h = button.size

                    if x < x_tip < x + w and y < y_tip < y + h:
                        button.drawbutton(img, color=(69, 69, 69))  # Highlight grey when hovering

                        # Calculate distance between index and middle fingertips
                        length, _, _ = detector.findDistance((x_tip, y_tip), (x_mid, y_mid), img)

                        if length is not None and length < 30 and not key_pressed:
                            if button.text == "DEL" and len(inputText) > 0:
                                inputText = inputText[:-1]  # Remove the last character
                            elif button.text == "SPACE":
                                inputText += " "  # Add space
                            elif button.text == "CAPS":
                                caps_lock = not caps_lock  # Toggle CAPS lock
                            elif button.text != "DEL" and len(inputText) < max_chars:
                                # Add character to input with CAPS lock logic
                                if caps_lock:
                                    inputText += button.text.upper()  # Add uppercase character
                                else:
                                    inputText += button.text.lower()  # Add lowercase character
                            button.drawbutton(img, color=(255, 0, 0))  # Turn blue when key is pressed
                            key_pressed = True
                            sleep(0.15)  # Delay to avoid repeated input

                    else:
                        button.drawbutton(img)  # Draw button with default color

                # Reset key_pressed when fingers are apart
                if length is not None and length >= 30:
                    key_pressed = False

    else:
        # No hands detected, draw default buttons
        for button in buttonSet:
            button.drawbutton(img)

    # Only draw the text box if the right hand is used
    if not left_hand_detected:
        # Draw input text box beneath the keyboard and control keys
        cv2.rectangle(img, (50, 500), (900, 550), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, inputText, (60, 540), cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

    # Show the image with updated layout
    cv2.imshow("Image", img)
    cv2.waitKey(1)
