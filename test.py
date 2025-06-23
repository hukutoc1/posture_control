import cv2
from Core.sensors.Camera import Camera
from Core.posture_analyzer import analyze_posture


def main():
    camera = Camera(camera_index=0)

    try:
        while True:
            frame, points, status = camera.get_data()
            if frame is not None:
                cv2.imshow("Camera", frame)

                result = analyze_posture(points)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        camera.stop()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
