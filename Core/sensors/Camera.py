import cv2
import mediapipe as mp
from Core.sensors.Sensor import Sensor
from Core.Points import Points
from Core.posture_analyzer import analyze_posture

mp_pose = mp.solutions.pose


class Camera(Sensor):
    """@brief Camera sensor class for posture analysis using MediaPipe.

       This class handles video capture, pose estimation, and posture analysis.
       Inherits from the base Sensor class.
    """
    def __init__(self, camera_index=0):
        """@brief Initialize the Camera sensor.

           @param camera_index Index of the camera to use (default: 0).
        """
        self.cap = cv2.VideoCapture(camera_index)
        self.pose = mp_pose.Pose(static_image_mode=False,
                                 model_complexity=1)

    def start(self):
        """@brief Start the camera capture.

           Opens the camera if it's not already open.
        """
        if not self.cap.isOpened():
            self.cap.open(0)

    def stop(self):
        """@brief Stop the camera capture and release resources."""
        self.cap.release()

    def get_data(self):
        """@brief Capture and process a frame for posture analysis.

           @return Tuple containing:
                   - frame: Captured video frame
                   - points: Detected landmark points (None if not detected)
                   - posture_status: Analysis result (None if no landmarks)
           Returns None if frame capture fails.
        """
        ret, frame = self.cap.read()
        h, w, _ = frame.shape

        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            points = Points(results.pose_landmarks.landmark)
            posture_status = analyze_posture(points, w, h)
            return frame, points, posture_status
        else:
            return frame, None, None
