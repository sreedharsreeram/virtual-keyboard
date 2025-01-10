import cv2
import cvzone
import numpy as np
from time import sleep
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Controller, Key  # Fixed import for Key

videocap = cv2.VideoCapture(0)
videocap.set(3, 1280)
videocap.set(4, 720)

detector = HandDetector(detectionCon=0.8)

key = [
    ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
    ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]
]

inputText = ""
max_chars = 15
caps_lock = False
keyboard = Controller()


class Buttons:
    def __init__(self, pos, text, size=[65, 65]):
        self.pos = pos
        self.size = size
        self.text = text

    def drawbutton(self, img, color=(0, 0, 0)):
        x, y = self.pos
        w, h = self.size
        overlay = img.copy()
        cv2.rectangle(overlay, self.pos, (x + w, y + h), color, cv2.FILLED)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)
        font_scale = 1.5 if self.text != "DEL" else 1.2
        cv2.putText(img, self.text, (x + 15, y + 50), cv2.FONT_ITALIC, font_scale, (255, 255, 255), 3)
        return img


buttonSet = []

for row_index, row in enumerate(key):
    for col_index, letter in enumerate(row):
        button_pos = [80 * col_index + 15, 70 * row_index + 50]
        button_size = [65, 65]
        buttonSet.append(Buttons(button_pos, letter, button_size))

buttonSet.append(Buttons([20, 360], "DEL", [150, 65]))
buttonSet.append(Buttons([190, 360], "SPACE", [400, 65]))
buttonSet.append(Buttons([600, 360], "CAPS", [150, 65]))

key_pressed = False

while True:
    success, img = videocap.read()
    hands, img = detector.findHands(img)
    length = None

    left_hand_detected = False
    right_hand_detected = False

    if hands:
        for hand in hands:
            if hand["type"] == "Right":
                right_hand_detected = True
            if hand["type"] == "Left":
                left_hand_detected = True

        if left_hand_detected:
            cv2.putText(img, "Please use your right hand", (200, 50), cv2.FONT_ITALIC, 1.5, (0, 0, 255), 3)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            continue

        if right_hand_detected:
            lmList = hands[0]["lmList"]
            if lmList:
                x_tip, y_tip = lmList[8][:2]
                x_mid, y_mid = lmList[12][:2]

                for button in buttonSet:
                    x, y = button.pos
                    w, h = button.size

                    if x < x_tip < x + w and y < y_tip < y + h:
                        button.drawbutton(img, color=(69, 69, 69))

                        length, _, _ = detector.findDistance((x_tip, y_tip), (x_mid, y_mid), img)

                        if length is not None and length < 30 and not key_pressed:
                            if button.text == "SPACE":
                                keyboard.press(Key.space)  # Use Key.space for spacebar
                            else:
                                keyboard.press(button.text)

                            if button.text == "DEL" and len(inputText) > 0:
                                inputText = inputText[:-1]
                            elif button.text == "SPACE":
                                inputText += " "
                            elif button.text == "CAPS":
                                caps_lock = not caps_lock
                            elif button.text != "DEL" and len(inputText) < max_chars:
                                if caps_lock:
                                    inputText += button.text.upper()
                                else:
                                    inputText += button.text.lower()

                            button.drawbutton(img, color=(255, 0, 0))
                            key_pressed = True
                            sleep(0.15)

                    else:
                        button.drawbutton(img)

                if length is not None and length >= 30:
                    key_pressed = False

    else:
        for button in buttonSet:
            button.drawbutton(img)

    if not left_hand_detected:
        cv2.rectangle(img, (50, 500), (900, 550), (0, 0, 0), cv2.FILLED)
        cv2.putText(img, inputText, (60, 540), cv2.FONT_ITALIC, 1, (255, 255, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
