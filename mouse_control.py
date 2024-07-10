import cv2
import numpy as np
import pyautogui
import mediapipe as mp

def mouse_control():
    global m_analysis_active
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

    cap = cv2.VideoCapture(0)
    m_analysis_active = True

    smoothening = 5
    frameR = 100  # Frame Reduction
    prev_x, prev_y = 0, 0
    curr_x, curr_y = 0, 0

    screen_width, screen_height = pyautogui.size()

    while m_analysis_active and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Flip the frame
        height, width, _ = frame.shape

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                lmList = []
                for id, lm in enumerate(hand_landmarks.landmark):
                    cx, cy = int(lm.x * width), int(lm.y * height)
                    lmList.append([id, cx, cy])
                    cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

                if lmList:
                    x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip
                    x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip

                    # Check which fingers are up
                    fingers = []
                    if lmList[8][2] < lmList[6][2]: fingers.append(1)  # Index finger
                    else: fingers.append(0)
                    if lmList[12][2] < lmList[10][2]: fingers.append(1)  # Middle finger
                    else: fingers.append(0)

                    # Only Index Finger: Moving Mode
                    if fingers[0] == 1 and fingers[1] == 0:
                        # Convert Coordinates
                        x3 = np.interp(x1, (frameR, width - frameR), (0, screen_width))
                        y3 = np.interp(y1, (frameR, height - frameR), (0, screen_height))

                        # Smoothen Values
                        curr_x = prev_x + (x3 - prev_x) / smoothening
                        curr_y = prev_y + (y3 - prev_y) / smoothening

                        # Move Mouse
                        if abs(curr_x - prev_x) > 5 or abs(curr_y - prev_y) > 5:  # Minimum movement threshold
                            pyautogui.moveTo(curr_x, curr_y)  # Remove the screen width flipping
                        prev_x, prev_y = curr_x, curr_y

                    # Both Index and Middle fingers are up: Clicking Mode
                    if fingers[0] == 1 and fingers[1] == 1:
                        # Find distance between fingers
                        distance = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                        if distance < 40:
                            pyautogui.click()

                cv2.rectangle(frame, (frameR, frameR), (width - frameR, height - frameR), (255, 0, 255), 2)

        cv2.imshow("Mouse Control", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the function
mouse_control()
