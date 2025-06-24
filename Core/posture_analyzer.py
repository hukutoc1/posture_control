from math import atan2, degrees
from Core.nose_shoulder_ratio_func import nose_shoulder_ratio


def analyze_posture(points, w, h, nose_to_shoulder_ratio=0.33):
    if points is None:
        return {"status": "bad", "message": "Landmarks are missing"}

    try:
        left_shoulder = points[11]
        right_shoulder = points[12]

        scale = max(w, h)

        xl = left_shoulder.x * w / scale
        yl = left_shoulder.y * h / scale

        xr = right_shoulder.x * w / scale
        yr = right_shoulder.y * h / scale

        dx = abs(xr - xl)
        dy = abs(yr - yl)

        angle_deg = degrees(atan2(dy, dx))

        ratio = nose_shoulder_ratio(points)

        if angle_deg > 5:
            return {"status": "bad", "message": f"Side shoulder tilt"}
        elif abs(ratio - nose_to_shoulder_ratio) > 0.15:
            return {"status": "bad", "message": f"Front tilt"}
        else:
            return {"status": "good", "message": "Success"}
    except Exception as e:
        return {"status": "error", "message": e}
