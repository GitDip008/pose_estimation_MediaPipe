import cv2
import numpy as np
import time
import PoseModule as pm


cap = cv2.VideoCapture("videos/6.mp4")
detector = pm.PoseDetector()

count = 0
direction = 0       # 0 when the hand is going up
previous_time = 0

while True:
    success, img = cap.read()
    if not success:
        print("No more frame available")
        break
    img = cv2.resize(img, (1280, 720))
    # img = cv2.imread("videos/1.jpeg")
    img = detector.find_pose(img, draw=False)
    landmarks = detector.find_position(img, draw=False)
    # print(landmarks)

    if len(landmarks) != 0:
        # # Right arm
        # angle = detector.find_angle(img, 12, 14, 16)
        # Left arm
        angle = detector.find_angle(img, 11, 13, 15)
        # percentage = np.interp(angle, (205, 320), (0, 100))
        if angle > 180:
            percentage = np.interp(angle, (205, 320), (0, 100))
            bar = np.interp(angle, (205, 320), (650, 100))
        else:
            percentage = np.interp(angle, (40, 120), (0, 100))
            bar = np.interp(angle, (40, 120), (650, 100))

        # print(angle, "--", percentage)

        # Check the dumbbell curls

        if percentage == 100:
            if direction == 0:
                count += 0.5
                direction = 1

        if percentage == 0:
            if direction == 1:
                count += 0.5
                direction = 0

        print(count)

        # Draw Bar
        cv2.rectangle(img, (1150, 100), (1225, 650), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(img, (1150, int(bar)), (1225, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(percentage)}%', (1145, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 4)

        # Draw Dumbbell counts
        cv2.rectangle(img, (0, 450), (250, 720), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'Dumbbell Count:', (30, 500), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 0), 2)
        cv2.putText(img, f'{int(count)}', (70, 645), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 25)


    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS: {int(fps)}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 4)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break