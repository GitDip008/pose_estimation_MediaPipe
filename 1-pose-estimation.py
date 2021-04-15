import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_draw = mp.solutions.drawing_utils


cap = cv2.VideoCapture("videos/4.mp4")
# cap = cv2.VideoCapture(0)

previous_time = 0
while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)
    # print(results.pose_landmarks)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            print(id, lm)
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)



    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

