import cv2
import mediapipe as mp
from Core.sensors.Sensor import Sensor
from Core.Points import Points
from Core.posture_analyzer import analyze_posture

mp_pose = mp.solutions.pose


class Camera(Sensor):
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        self.pose = mp_pose.Pose(static_image_mode=False,
                                 model_complexity=1)

    def start(self):
        if not self.cap.isOpened():
            self.cap.open(0)

    def stop(self):
        self.cap.release()

    def get_data(self):
        ret, frame = self.cap.read()

        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            points = Points(results.pose_landmarks.landmark)
            posture_status = analyze_posture(points)
            return frame, points, posture_status
        else:
            return frame, None, None
