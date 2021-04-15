import cv2
import time
import PoseModule as pm

cap = cv2.VideoCapture("videos/4.mp4")
# cap = cv2.VideoCapture(0)

previous_time = 0
detector = pm.PoseDetector()

while True:
    success, img = cap.read()
    if not success:
        print("No more frame available")
        break
    # img = cv2.flip(img, 1)
    # print(img.shape)
    h, w, c = img.shape
    img = cv2.resize(img, (int(w/1.5), int(h/1.5)))

    img = detector.find_pose(img)
    landmark_list = detector.find_position(img, draw=False)
    # if len(landmark_list) != 0:
    #     print(landmark_list)
    #     cv2.circle(img, (landmark_list[0][1], landmark_list[0][2]), 5, (255, 0, 0), cv2.FILLED)

    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time
    cv2.putText(img, f'FPS: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Image", img)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
