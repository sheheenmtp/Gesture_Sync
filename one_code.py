import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import os
import speech_recognition as sr
import threading

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

volume_control_active = False
app_control_active = False
exit_program = False

def activate_function(command):
    global volume_control_active, app_control_active, exit_program
    if "volume control" in command:
        print("Volume control activated")
        volume_control_active = True
    elif "deactivate volume control" in command:
        print("Volume control deactivated")
        volume_control_active = False
    elif "app control" in command:
        print("App control activated")
        app_control_active = True
    elif "deactivate app control" in command:
        print("App control deactivated")
        app_control_active = False
    elif "exit" in command:
        print("Exiting program...")
        exit_program = True
    else:
        print("Command not recognized")

def voice_recognition():
    recognizer = sr.Recognizer()
    while not exit_program:
        with sr.Microphone() as source:
            print("Say a command...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

            try:
                command = recognizer.recognize_google(audio).lower()
                print("You said:", command)
                activate_function(command)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

def volume_control():
    global volume_control_active
    cap = cv2.VideoCapture(0)
    prev_distance = 50
    volume_step = 2

    while not exit_program:
        if volume_control_active:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    thumb_x, thumb_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
                    index_x, index_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

                    distance = np.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2 // 4)

                    if distance > prev_distance:
                        pyautogui.press('volumeup', presses=volume_step)
                    else:
                        pyautogui.press('volumedown', presses=volume_step)

                    cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
                    cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)
                    cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 255), 2)

            cv2.imshow('Volume Control', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

def finger_analysis():
    global app_control_active
    cap = cv2.VideoCapture(0)

    while not exit_program:
        if app_control_active:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                    ring_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
                    pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

                    fingers_up = 0
                    if index_tip.y < thumb_tip.y:
                        fingers_up += 1
                    if middle_tip.y < thumb_tip.y:
                        fingers_up += 1
                    if ring_tip.y < thumb_tip.y:
                        fingers_up += 1
                    if pinky_tip.y < thumb_tip.y:
                        fingers_up += 1

                    if fingers_up == 3:
                        os.system("start chrome")
                    elif fingers_up == 4:
                        os.system("TASKKILL /F /IM chrome.exe")

            cv2.imshow('Finger Analysis', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Start voice recognition in a separate thread
    voice_thread = threading.Thread(target=voice_recognition)
    voice_thread.start()

    # Start volume control and app control in the main thread
    volume_control()
    finger_analysis()
