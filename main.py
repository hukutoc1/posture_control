import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import time
from Core.nose_shoulder_ratio_func import nose_shoulder_ratio
from Core.sensors.Camera import Camera
from Core.posture_analyzer import analyze_posture


class CameraApp:
    def __init__(self, root, camera):
        """Class constructor.

            Initializes the main application window and starts the camera feed.

            Args:
                root (Tk): The main Tkinter window object.
                camera (Camera): Camera object used for capturing and
                processing frames.
        """
        self.root = root
        self.camera = camera
        self.root.title("Posture Analysis")

        self.root.geometry("800x700")
        self.root.minsize(600, 750)

        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.video_frame = ttk.Label(self.main_frame)
        self.video_frame.pack(pady=10)

        self.calibration_label = ttk.Label(
            self.main_frame,
            text="",
            font=('Helvetica', 14)
        )
        self.calibration_label.pack(pady=10)

        self.status_frame = ttk.LabelFrame(self.main_frame,
                                           text="Posture Status")
        self.status_frame.pack(fill=tk.X, pady=10)

        self.status_label = ttk.Label(
            self.status_frame,
            text="Waiting for calibration...",
            font=('Helvetica', 12)
        )
        self.status_label.pack(pady=5)

        self.notification_label = ttk.Label(
            self.main_frame,
            text="",
            font=('Helvetica', 12),
            foreground='red'
        )
        self.notification_label.pack(pady=5)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)

        self.start_button = ttk.Button(
            self.button_frame,
            text="Start Calibration",
            command=self.start_calibration
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            self.button_frame,
            text="Stop",
            command=self.stop_camera,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.is_running = False
        self.is_calibrating = False
        self.calibration_complete = False
        self.reference_ratio = None
        self.reference_points = None
        self.frame_width = 0
        self.frame_height = 0

        self.notification_timer = None
        self.bad_posture_start_time = None
        self.no_person_start_time = None

        self.black_image = Image.new('RGB', (640, 480), (0, 0, 0))
        self.black_photo = ImageTk.PhotoImage(image=self.black_image)

        self.video_frame.configure(image=self.black_photo)
        self.video_frame.image = self.black_photo

    def start_calibration(self):
        """Initiates the posture calibration sequence.

        This method starts the calibration process, during which the user is
        expected to sit in a correct, upright posture. The system captures data
        to establish a reference ratio for future posture analysis.
        """
        if not self.is_running:
            try:
                self.camera.start()
                self.is_running = True
                self.is_calibrating = True
                self.calibration_complete = False
                self.start_button.config(state=tk.DISABLED)
                self.stop_button.config(state=tk.NORMAL)

                self.calibration_label.config(
                    text="Please sit straight for calibration...")
                self.status_label.config(text="Calibrating...")
                self.root.after(3000, self.capture_reference)
            except Exception as e:
                messagebox.showerror("Error",
                                     f"Failed to start camera: "
                                     f"{str(e)}")
                self.stop_camera()

    def capture_reference(self):
        """Captures and stores the reference posture position.

        This method is typically called during calibration. It captures the
        current
        body landmarks (e.g., nose and shoulders) and computes a reference
        ratio used for future posture analysis.
        """
        if self.is_running and self.is_calibrating:
            data = self.camera.get_data()

            if data is not None and data[1] is not None:
                frame, points, _ = data
                self.frame_height, self.frame_width, _ = frame.shape
                self.reference_ratio = nose_shoulder_ratio(points)
                self.reference_points = points

                self.calibration_label.config(
                    text="Calibration complete! Reference position saved.")
                self.status_label.config(
                    text="Calibration complete. Starting analysis...")

                self.is_calibrating = False
                self.calibration_complete = True

                self.root.after(2000,
                                lambda: self.calibration_label.config(text=""))
                self.start_analysis()
            else:
                self.calibration_label.config(
                    text="No person detected. Trying again...")
                self.root.after(1000, self.capture_reference)

    def start_analysis(self):
        """@brief Begins continuous posture analysis"""
        if self.is_running and self.calibration_complete:
            self.status_label.config(text="Analyzing posture...")
            self.update_frame()

    def stop_camera(self):
        """@brief Stops camera capture and resets application state"""
        if self.is_running:
            self.camera.stop()
            self.is_running = False
            self.is_calibrating = False
            self.calibration_complete = False

            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

            self.video_frame.configure(image=self.black_photo)
            self.video_frame.image = self.black_photo

            self.status_label.config(text="Waiting for calibration...")
            self.clear_notification()

            if self.notification_timer:
                self.root.after_cancel(self.notification_timer)
                self.notification_timer = None

            self.bad_posture_start_time = None
            self.no_person_start_time = None

    def clear_notification(self):
        """@brief Clears any active notification messages"""
        if self.notification_label.winfo_exists():
            self.notification_label.config(text="")

    def show_notification(self, message):
        """@brief Displays a notification message with auto-clear
           @param message Text message to display
        """
        if not self.notification_label.winfo_exists():
            return

        self.notification_label.config(text=message)
        messagebox.showwarning("Posture Alert", message)

        self.root.after(3000, self.clear_notification)

    def check_posture_problems(self, result, no_person_detected):
        """@brief Monitors for posture issues and triggers notifications
           @param result Dictionary containing posture analysis results
           @param no_person_detected Boolean indicating if person is detected
        """
        current_time = time.time()

        if no_person_detected:
            if self.no_person_start_time is None:
                self.no_person_start_time = current_time
                self.bad_posture_start_time = None
            elif (current_time - self.no_person_start_time) >= 5:
                self.show_notification(
                    "Warning: No person detected for 5 seconds!")
                self.no_person_start_time = None
        else:
            if self.no_person_start_time is not None:
                self.no_person_start_time = None
                self.clear_notification()

            if result:
                if result.get('status') != 'good':
                    if self.bad_posture_start_time is None:
                        self.bad_posture_start_time = current_time
                    elif (current_time - self.bad_posture_start_time) >= 5:
                        self.show_notification(
                            f"Warning: Bad posture detected!\n"
                            f"Status: {result['status']}\n"
                            f"Message: {result.get('message', '')}"
                        )
                        self.bad_posture_start_time = None
                else:
                    if self.bad_posture_start_time is not None:
                        self.bad_posture_start_time = None
                        self.clear_notification()

    def update_frame(self):
        """@brief Main video processing loop."""
        if self.is_running and self.calibration_complete:
            data = self.camera.get_data()

            if data is not None:
                frame, points, _ = data

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)

                self.video_frame.imgtk = imgtk
                self.video_frame.configure(image=imgtk)
                self.video_frame.image = imgtk

                if points is not None:
                    result = analyze_posture(
                        points,
                        self.frame_width,
                        self.frame_height,
                        nose_to_shoulder_ratio=self.reference_ratio
                    )

                    status_text = ""
                    if result:
                        status_text = \
                            f"Status: {result.get('status', 'unknown')}\n"
                        if 'message' in result:
                            status_text += f"Message: {result['message']}\n"
                        if 'angles' in result:
                            for (angle_name,
                                 angle_value) in result['angles'].items():
                                status_text += \
                                    f"{angle_name}: {angle_value:.1f}\n"

                    self.status_label.config(text=status_text)

                    self.check_posture_problems(result,
                                                no_person_detected=False)
                else:
                    self.status_label.config(text="No person detected")
                    self.check_posture_problems(None, no_person_detected=True)

            self.notification_timer = self.root.after(10, self.update_frame)


if __name__ == "__main__":
    root = tk.Tk()
    camera = Camera()
    app = CameraApp(root, camera)


    def on_closing():
        app.stop_camera()
        root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
