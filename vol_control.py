import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import threading

# Global variable to track the status of volume analysis
v_analysis_active = False

def volume_control():
    global v_analysis_active
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    v_analysis_active = True

    prev_distance = 50
    volume_step = 2

    while v_analysis_active and cap.isOpened():  # Check if analysis is active and the capture is open
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

                distance = np.sqrt((thumb_x - index_x) ** 2 + (thumb_y - index_y) ** 2//4)

                if distance > prev_distance:
                    pyautogui.press('volumeup', presses=volume_step)
                else:
                    pyautogui.press('volumedown', presses=volume_step)

                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 0), -1)
                cv2.circle(frame, (index_x, index_y), 10, (0, 0, 255), -1)
                cv2.line(frame, (thumb_x, thumb_y), (index_x, index_y), (255, 255, 255), 2)

        # cv2.imshow('Volume Control', frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to deactivate volume analysis
def v_deactivate_analysis():
    global v_analysis_active
    v_analysis_active = False

# Example of how to activate and deactivate volume control
if __name__ == "__main__":
    # Start volume control in a separate thread
    volume_thread = threading.Thread(target=volume_control)
    volume_thread.start()

    # Simulate deactivating volume control after 5 seconds
    # threading.Timer(5, v_deactivate_analysis).start()
