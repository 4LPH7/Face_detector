import face_recognition
import os


class FaceProcessor:
    """
    Handles face detection, recognition, and database management.
    """

    def __init__(self, known_faces_dir="known_faces"):
        self.known_faces_encodings = []
        self.known_faces_names = []
        self.known_faces_dir = known_faces_dir
        self.load_known_faces()

    def load_known_faces(self):
        """Load known faces from the directory."""
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".png")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.known_faces_dir, filename)
                self.add_known_face(image_path, name)

    def add_known_face(self, image_path, name):
        """Add a new face to the known faces database."""
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                encoding = encodings[0]
                self.known_faces_encodings.append(encoding)
                self.known_faces_names.append(name)
                print(f"Added {name} to known faces.")
            else:
                print(f"No face detected in {image_path}. Skipping.")
        except Exception as e:
            print(f"Error processing {image_path}: {e}")