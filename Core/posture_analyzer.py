from math import atan2, degrees
from Core.nose_shoulder_ratio_func import nose_shoulder_ratio


def analyze_posture(points, w, h, nose_to_shoulder_ratio=0.33):
    """@brief Analyze posture based on shoulder landmarks and nose-to-shoulder
              ratio.

        @param points List of landmark points (expected to contain shoulder
               points).
        @param w Width of the frame (used for normalization).
        @param h Height of the frame (used for normalization).
        @param nose_to_shoulder_ratio Expected ratio for started posture
               (default: 0.33).
        @return Dictionary with posture analysis result:
        - "status": "good" (correct posture), "bad" (detected tilt),
        or "error".
        - "message": Detailed status description or error message.
    """
    if points is None:
        return {"status": "bad", "message": "Landmarks are missing"}

    try:
        # Left shoulder landmark point
        left_shoulder = points[11]
        # Right shoulder landmark point
        right_shoulder = points[12]

        # Normalization scale (largest dimension)
        scale = max(w, h)

        # Normalized left shoulder coordinates
        xl = left_shoulder.x * w / scale
        yl = left_shoulder.y * h / scale

        # Normalized right shoulder coordinates
        xr = right_shoulder.x * w / scale
        yr = right_shoulder.y * h / scale

        # Absolute differences in x and y coordinates
        dx = abs(xr - xl)
        dy = abs(yr - yl)

        # Shoulder tilt angle (degrees)
        angle_deg = degrees(atan2(dy, dx))

        # Nose-to-shoulder ratio (uses external function)
        ratio = nose_shoulder_ratio(points)

        # Posture evaluation logic
        if angle_deg > 5:
            return {"status": "bad", "message": f"Side shoulder tilt"}
        elif abs(ratio - nose_to_shoulder_ratio) > 0.15:
            return {"status": "bad", "message": f"Front tilt"}
        else:
            return {"status": "good", "message": "Success"}
    except Exception as e:
        return {"status": "error", "message": e}
