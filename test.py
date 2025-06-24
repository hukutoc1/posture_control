import cv2
from Core.sensors.Camera import Camera
from Core.posture_analyzer import analyze_posture
from Core.nose_shoulder_ratio_func import nose_shoulder_ratio


def main():
    camera = Camera(camera_index=0)

    try:
        frame, points, status = camera.get_data()
        rt = nose_shoulder_ratio(points)
        h, w, _ = frame.shape
        result = analyze_posture(points, w, h,
                                 nose_to_shoulder_ratio=rt)
        print(result)
        prev_res = result
        while True:
            frame, points, status = camera.get_data()
            if frame is not None:
                cv2.imshow("Camera", frame)

                result = analyze_posture(points, w, h,
                                         nose_to_shoulder_ratio=rt)
                if result["status"] != prev_res["status"]:
                    print(result)
                    prev_res = result

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()