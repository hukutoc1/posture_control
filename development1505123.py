import cv2
import time

def capture_with_low_fps(camera_index=0, output_fps=2, display=True):

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Ошибка: Не удалось подключиться к камере.")
        return

    last_capture_time = 0
    frame_interval = 1.0 / output_fps

    try:
        while True:
            current_time = time.time()
            if current_time - last_capture_time >= frame_interval:
                ret, frame = cap.read()
                if not ret:
                    print("Ошибка: Не удалось получить кадр.")
                    break

                last_capture_time = current_time

                if display:
                    cv2.imshow('Low FPS Camera', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                time.sleep(0.001)
    finally:
        cap.release()
        if display:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_with_low_fps(output_fps=2)