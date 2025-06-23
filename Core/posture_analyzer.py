nose_to_shoulder_distance = 1


def analyze_posture(points):
    if points is None:
        return {"status": "bad", "message": "Landmarks are missing"}

    try:
        left_shoulder = points[11]
        right_shoulder = points[12]

        nose = points[0]

        diff_shoulder = abs(left_shoulder.y - right_shoulder.y)

        if diff_shoulder > 0.1:
            return {"status": "bad", "message": "Side tilt"}
        elif nose.y - diff_shoulder > nose_to_shoulder_distance:
            return {"status": "bad", "message": "Front tilt"}
        else:
            return {"status": "good", "message": "Success"}
    except Exception as e:
        return "Ошибка данных"
