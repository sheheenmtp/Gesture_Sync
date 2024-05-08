import cv2
import mediapipe as mp
import os
import threading

# Global variable to track the status of gesture analysis
analysis_active = False

def hand_gesture_analysis():
    global analysis_active

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    analysis_active = True

    try:
        while analysis_active and cap.isOpened():  # Check if analysis is active and the capture is open
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

                    if fingers_up == 4:
                        os.system("start chrome")
                    elif fingers_up == 3:
                        os.system("TASKKILL /F /IM chrome.exe")

            # cv2.imshow('Finger Analysis', frame)

            if cv2.waitKey(1) & 0xFF == 27:  # Press ESC to exit
                break

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")
    finally:
        cap.release()
        cv2.destroyAllWindows()

# Function to deactivate gesture analysis
def deactivate_analysis():
    global analysis_active
    analysis_active = False

# Example of how to activate and deactivate gesture analysis
if __name__ == "__main__":
    # Start hand gesture analysis in a separate thread
    gesture_thread = threading.Thread(target=hand_gesture_analysis)
    gesture_thread.start()

    # Simulate deactivating gesture analysis after 5 seconds
    # threading.Timer(5, deactivate_analysis).start()
