import face_recognition
import os
import pickle
import logging


class FaceProcessor:
    """
    Handles face detection, recognition, and database management.
    """

    def __init__(self, known_faces_dir="known_faces", encodings_file="encodings.pkl"):
        self.known_faces_encodings = []
        self.known_faces_names = []
        self.known_faces_dir = known_faces_dir
        self.encodings_file = encodings_file
        self._setup_logging()
        self.load_known_faces()

    def _setup_logging(self):
        """Setup logging for feedback."""
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def load_known_faces(self):
        """Load known faces from file or directory."""
        if os.path.exists(self.encodings_file):
            try:
                with open(self.encodings_file, "rb") as f:
                    data = pickle.load(f)
                    self.known_faces_encodings = data["encodings"]
                    self.known_faces_names = data["names"]
                    self.logger.info("Loaded known faces from encodings file.")
                return
            except Exception as e:
                self.logger.error(f"Failed to load encodings file: {e}")

        # Fallback: Load from the directory
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith((".jpg", ".png")):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.known_faces_dir, filename)
                self.add_known_face(image_path, name)

    def save_encodings(self):
        """Save encodings to a file."""
        try:
            data = {"encodings": self.known_faces_encodings, "names": self.known_faces_names}
            with open(self.encodings_file, "wb") as f:
                pickle.dump(data, f)
            self.logger.info("Encodings saved successfully.")
        except Exception as e:
            self.logger.error(f"Failed to save encodings: {e}")

    def add_known_face(self, image_path, name):
        """Add a new face to the known faces database."""
        if not os.path.isfile(image_path):
            self.logger.warning(f"File not found: {image_path}")
            return
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                encoding = encodings[0]
                self.known_faces_encodings.append(encoding)
                self.known_faces_names.append(name)
                self.logger.info(f"Added {name} to known faces.")
                self.save_encodings()  # Save encodings after adding
            else:
                self.logger.warning(f"No face detected in {image_path}. Skipping.")
        except Exception as e:
            self.logger.error(f"Error processing {image_path}: {e}")
