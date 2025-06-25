import cv2
import mediapipe as mp
from Core.sensors.Sensor import Sensor
from Core.Points import Points
from Core.posture_analyzer import analyze_posture

mp_pose = mp.solutions.pose


class Camera(Sensor):
    """Camera sensor class for posture analysis using MediaPipe.

    This class handles video capture, pose estimation, and posture analysis.
    Implements the base Sensor interface for compatibility with the posture
    monitoring system.

    Attributes:
    cap (cv2.VideoCapture): OpenCV VideoCapture object for accessing the
    camera.
    pose (mp.solutions.Pose): MediaPipe Pose solution instance.
    """
    def __init__(self, camera_index=0):
        """Initialize the Camera sensor.

        Args:
            camera_index (int): Index of the camera to use (default: 0).
        """
        self.cap = cv2.VideoCapture(camera_index)
        self.pose = mp_pose.Pose(static_image_mode=False,
                                 model_complexity=1)

    def start(self):
        """Start the camera capture.

        Opens the camera if it's not already open.
        """
        if not self.cap.isOpened():
            self.cap.open(0)

    def stop(self):
        """Stop the camera capture and release resources."""
        self.cap.release()

    def get_data(self):
        """Capture and process a frame for posture analysis.

        Returns:
            Tuple containing:
                - frame (np.ndarray | None): Captured video frame (BGR format),
                 or None if capture fails.
                - points (Points | None): Detected landmark points, or None if
                not detected.
                - posture_status (str | None): Analysis result, or None if no
                landmarks are present.
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
