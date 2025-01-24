import cv2
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
import pickle
from datetime import datetime
import csv


class EnhancedFaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Face Recognition System")

        # Configuration
        self.KNOWN_FACES_DIR = "known_faces"
        self.ENCODINGS_FILE = "face_encodings.pkl"
        self.ATTENDANCE_FILE = "attendance.csv"
        self.MIN_CONFIDENCE = 0.5
        self.TOLERANCE = 60
        self.UNKNOWN_THRESHOLD = 5  # Frames before marking unknown

        # Initialize data structures
        self.known_encodings = {"encodings": [], "names": []}
        self.face_tracker = {}
        self.attendance_log = []

        # Create directories
        os.makedirs(self.KNOWN_FACES_DIR, exist_ok=True)

        # Load existing database
        self.load_face_database()
        self.load_attendance_log()

        # Initialize models
        self.initialize_models()

        # GUI Setup
        self.setup_gui()

        # Start video processing
        self.vid = cv2.VideoCapture(0)
        if not self.vid.isOpened():
            messagebox.showerror("Error", "Could not open video capture")
            self.root.destroy()
            return

        self.update_video()

    def initialize_models(self):
        # Face detection model
        self.prototxt = "deploy.prototxt"
        self.model = "res10_300x300_ssd_iter_140000_fp16.caffemodel"

        if not all(os.path.exists(f) for f in [self.prototxt, self.model]):
            messagebox.showerror("Error", "Missing model files")
            self.root.destroy()
            return

        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

    def setup_gui(self):
        # Video display
        self.video_label = tk.Label(self.root)
        self.video_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Attendance list
        self.attendance_list = tk.Listbox(control_frame, width=30, height=15)
        self.attendance_list.pack(pady=5)

        # Buttons
        ttk.Button(control_frame, text="Capture Faces", command=self.capture_faces).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Manage Database", command=self.manage_database).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Export Attendance", command=self.export_attendance).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Settings", command=self.show_settings).pack(fill=tk.X, pady=2)
        ttk.Button(control_frame, text="Quit", command=self.quit_app).pack(fill=tk.X, pady=2)

        # Status bar
        self.status_var = tk.StringVar()
        ttk.Label(control_frame, textvariable=self.status_var).pack(fill=tk.X, pady=5)

    def update_video(self):
        ret, frame = self.vid.read()
        if ret:
            processed_frame = self.process_frame(frame)
            self.display_frame(processed_frame)
        self.root.after(10, self.update_video)

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        detections = self.detect_faces(small_frame)

        current_names = []
        for (startX, startY, endX, endY), face_img in detections:
            if face_img.size == 0:
                continue

            name = self.recognize_face(face_img)
            current_names.append(name)

            # Scale coordinates
            top, right, bottom, left = [coord * 4 for coord in (startY, endX, endY, startX)]

            # Draw UI elements
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, bottom + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)

            # Update attendance
            self.update_attendance(name)

        # Track faces between frames
        self.update_face_tracker(current_names)
        return frame

    def detect_faces(self, frame):
        detections = []
        h, w = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                                     (300, 300), (104.0, 177.0, 123.0))
        self.net.setInput(blob)
        results = self.net.forward()

        for i in range(results.shape[2]):
            confidence = results[0, 0, i, 2]
            if confidence > self.MIN_CONFIDENCE:
                box = results[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                # Expand face area
                startX, startY = max(0, startX - 20), max(0, startY - 20)
                endX, endY = min(w, endX + 20), min(h, endY + 20)

                face_img = frame[startY:endY, startX:endX]
                if face_img.size > 0:
                    detections.append(((startX, startY, endX, endY), face_img))

        return detections

    def recognize_face(self, face_img):
        if not self.known_encodings["encodings"]:
            return "Unknown"

        # Improved encoding using LBP histogram
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        lbp = self.local_binary_pattern(gray)
        hist = cv2.calcHist([lbp], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        # Ensure histograms are the same size
        if hist.size != self.known_encodings["encodings"][0].size:
            return "Unknown"

        # Compare with known encodings
        distances = []
        for e in self.known_encodings["encodings"]:
            if e.size == hist.size:
                distances.append(cv2.compareHist(hist, e, cv2.HISTCMP_CHISQR))

        if not distances:
            return "Unknown"

        min_dist = min(distances)
        if min_dist < self.TOLERANCE:
            return self.known_encodings["names"][distances.index(min_dist)]
        return "Unknown"

    def local_binary_pattern(self, img, radius=3, neighbors=24):
        # Initialize LBP as float to avoid overflow
        lbp = np.zeros_like(img, dtype=np.float32)
        for n in range(neighbors):
            x = radius * np.cos(2 * np.pi * n / neighbors)
            y = radius * np.sin(2 * np.pi * n / neighbors)

            fx = np.floor(x).astype(int)
            fy = np.floor(y).astype(int)
            cx = np.ceil(x).astype(int)
            cy = np.ceil(y).astype(int)

            # Calculate interpolation weights
            wx = x - fx
            wy = y - fy

            # Interpolate pixel values
            interp = (1 - wx) * (1 - wy) * img + wx * (1 - wy) * img + (1 - wx) * wy * img + wx * wy * img

            # Update LBP
            lbp += (interp >= img).astype(np.float32) * (1 << n)

        # Convert back to uint8
        return lbp.astype(np.uint8)

    def update_face_tracker(self, current_names):
        # Update tracker and handle unknowns
        for name in current_names:
            if name not in self.face_tracker:
                self.face_tracker[name] = {"count": 0, "timestamp": datetime.now()}
            self.face_tracker[name]["count"] += 1

        # Remove stale entries
        stale = [name for name, data in self.face_tracker.items()
                 if (datetime.now() - data["timestamp"]).seconds > 5]
        for name in stale:
            del self.face_tracker[name]

    def update_attendance(self, name):
        if name == "Unknown":
            return

        existing = next((entry for entry in self.attendance_log
                         if entry["name"] == name), None)
        if not existing:
            self.attendance_log.append({
                "name": name,
                "first_seen": datetime.now(),
                "last_seen": datetime.now()
            })
            self.attendance_list.insert(tk.END,
                                        f"{name} - {datetime.now().strftime('%H:%M:%S')}")
        else:
            existing["last_seen"] = datetime.now()

    def capture_faces(self):
        ret, frame = self.vid.read()
        if not ret:
            return

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        detections = self.detect_faces(small_frame)

        if not detections:
            messagebox.showinfo("Info", "No faces detected")
            return

        for (startX, startY, endX, endY), face_img in detections:
            name = simpledialog.askstring("New Face",
                                          "Enter name for detected face:", parent=self.root)
            if name:
                self.register_face(face_img, name)

        self.status_var.set(f"Registered {len(detections)} new faces")

    def register_face(self, face_img, name):
        filename = f"{self.KNOWN_FACES_DIR}/{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
        cv2.imwrite(filename, cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))

        # Create LBP encoding
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        lbp = self.local_binary_pattern(gray)
        hist = cv2.calcHist([lbp], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()

        self.known_encodings["encodings"].append(hist)
        self.known_encodings["names"].append(name)
        self.save_face_database()

    def manage_database(self):
        manage_win = tk.Toplevel(self.root)
        manage_win.title("Manage Database")

        listbox = tk.Listbox(manage_win, width=40)
        listbox.pack(padx=10, pady=10)

        for name in set(self.known_encodings["names"]):
            listbox.insert(tk.END, name)

        ttk.Button(manage_win, text="Delete Selected",
                   command=lambda: self.delete_face(listbox)).pack(pady=5)

    def delete_face(self, listbox):
        selection = listbox.curselection()
        if not selection:
            return

        name = listbox.get(selection[0])
        # Remove all entries with this name
        indices = [i for i, n in enumerate(self.known_encodings["names"]) if n == name]

        for i in reversed(indices):
            del self.known_encodings["encodings"][i]
            del self.known_encodings["names"][i]

        self.save_face_database()
        listbox.delete(selection[0])
        messagebox.showinfo("Info", f"Deleted all entries for {name}")

    def export_attendance(self):
        with open(self.ATTENDANCE_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            for entry in self.attendance_log:
                writer.writerow([
                    entry["name"],
                    entry["first_seen"].isoformat(),
                    entry["last_seen"].isoformat()
                ])
        self.status_var.set(f"Exported attendance to {self.ATTENDANCE_FILE}")

    def show_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("System Settings")

        ttk.Label(settings_win, text="Recognition Tolerance:").grid(row=0, column=0, padx=5, pady=2)
        tolerance_scale = ttk.Scale(settings_win, from_=0, to=100,
                                    value=self.TOLERANCE, command=lambda v: self.update_tolerance(v))
        tolerance_scale.grid(row=0, column=1, padx=5, pady=2)

        ttk.Label(settings_win, text="Confidence Threshold:").grid(row=1, column=0, padx=5, pady=2)
        confidence_scale = ttk.Scale(settings_win, from_=0, to=1,
                                     value=self.MIN_CONFIDENCE, command=lambda v: self.update_confidence(v))
        confidence_scale.grid(row=1, column=1, padx=5, pady=2)

    def update_tolerance(self, value):
        self.TOLERANCE = float(value)

    def update_confidence(self, value):
        self.MIN_CONFIDENCE = float(value)

    def load_face_database(self):
        if os.path.exists(self.ENCODINGS_FILE):
            with open(self.ENCODINGS_FILE, "rb") as f:
                self.known_encodings = pickle.load(f)

    def save_face_database(self):
        with open(self.ENCODINGS_FILE, "wb") as f:
            pickle.dump(self.known_encodings, f)

    def load_attendance_log(self):
        if os.path.exists(self.ATTENDANCE_FILE):
            with open(self.ATTENDANCE_FILE, "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.attendance_log.append({
                        "name": row[0],
                        "first_seen": datetime.fromisoformat(row[1]),
                        "last_seen": datetime.fromisoformat(row[2])
                    })

    def display_frame(self, frame):
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

    def quit_app(self):
        self.vid.release()
        self.save_face_database()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedFaceRecognitionApp(root)
    root.mainloop()