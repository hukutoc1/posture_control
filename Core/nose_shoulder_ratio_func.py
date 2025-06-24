from math import hypot


def nose_shoulder_ratio(points):
    try:
        left_shoulder = points[11]
        right_shoulder = points[12]
        nose = points[0]
        mid_y = (left_shoulder.y + right_shoulder.y) / 2

        nose_to_should = nose.y - mid_y

        shoulder_width = hypot(left_shoulder.x - right_shoulder.x,
                               left_shoulder.y - right_shoulder.y)

        if shoulder_width == 0:
            return None

        return nose_to_should / shoulder_width
    except Exception:
        return None
