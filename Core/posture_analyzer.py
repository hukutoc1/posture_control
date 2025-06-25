from math import atan2, degrees
from Core.nose_shoulder_ratio_func import nose_shoulder_ratio


def analyze_posture(points, w, h, nose_to_shoulder_ratio=0.33):
    """Analyze posture based on shoulder landmarks and nose-to-shoulder ratio.

    Args:
        points (list): List of landmark points (expected to contain shoulder points).
        w (int): Width of the frame (used for normalization).
        h (int): Height of the frame (used for normalization).
        nose_to_shoulder_ratio (float, optional): Expected ratio for upright posture.
            Defaults to 0.33 if not provided.

    Returns:
        dict: Dictionary with posture analysis result. Contains:
            - "status" (str): "good", "bad", or "error".
            - "message" (str): Detailed description of the posture status.
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
