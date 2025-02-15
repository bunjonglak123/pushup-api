import cv2
import mediapipe as mp
import threading
import time

from components.push_up.exercise_type import push_up
from utils.tools import start_timer

timer_done = False
# cap = cv2.VideoCapture("video.mp4")  # เปลี่ยนเป็น 0 หากต้องการใช้กล้องเว็บแคม
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ไม่สามารถเข้าถึงกล้องได้")
    # exit()

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def timer_function(timeStart):
    global timer_done
    start_timer(timeStart)
    timer_done = True

def getExerciseAll(timeStart, exerciseType):
    global timer_done, cap
    count = 0
    position = "up"

    # เริ่ม timer ใน thread แยก
    timer_thread = threading.Thread(target=timer_function, args=(timeStart,))
    timer_thread.daemon = True
    timer_thread.start()
    print('Frame ใช้งาน : 1 ')
    # เริ่ม MediaPipe Pose
    with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
        print('Frame ใช้งาน : 2 ')
        print("cap : ", cap)
        print("cap : ", cap.isOpened())
        while cap.isOpened():
            print('Frame ใช้งาน : 3')
            success, frame = cap.read()
            if not success:
                print("Frame ว่าง เปลี่ยนไปใช้ frame ถัดไปหรือจบวิดีโอ")
                break
            print('Frame ใช้งาน : 4')

            # ทำ mirror effect และแปลงสีสำหรับประมวลผล
            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(image_rgb)
            imlist = []

            if result.pose_landmarks:
                # วาด landmarks บน frame
                mp_drawing.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)
                for id, landmark in enumerate(result.pose_landmarks.landmark):
                    h, w, _ = frame.shape
                    X, Y = int(landmark.x * w), int(landmark.y * h)
                    imlist.append([id, X, Y])

            # นับ push-up หากมี landmark ที่ตรวจจับได้
            if imlist and exerciseType == "push_up":
                count, position = push_up(imlist, count, position)

            # ตรวจสอบการสิ้นสุด timer
            if timer_done:
                break

            # เข้ารหัส frame เป็น JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue

            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    cap.release()
