import cv2
import face_recognition
from face_processor import FaceProcessor
from counter import PeopleCounter
from utils import save_statistics


def main():
    # Initialize video capture
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Initialize processors
    face_processor = FaceProcessor()
    people_counter = PeopleCounter()

    frame_count = 0
    process_every_n_frames = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break

        # Process every nth frame
        if frame_count % process_every_n_frames == 0:
            # Resize frame for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = small_frame[:, :, ::-1]

            # Find faces
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(face_processor.known_faces_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = face_processor.known_faces_names[first_match_index]
                names.append(name)

            # Draw rectangles and labels
            for (top, right, bottom, left), name in zip(face_locations, names):
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

            # Count people
            count = people_counter.update_count(face_locations)
            cv2.putText(frame, f'People Count: {count}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            save_statistics(count)

        # Display frame
        cv2.imshow('Video', frame)
        frame_count += 1

        # Key controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('a'):
            name = input("Enter the name: ")
            # Capture and save face
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            if len(face_locations) == 0:
                print("No face detected.")
            else:
                top, right, bottom, left = face_locations[0]
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                face_image = frame[top:bottom, left:right]
                cv2.imwrite(os.path.join(face_processor.known_faces_dir, f"{name}.jpg"), face_image)
                print(f"Face of {name} saved.")
                face_processor.load_known_faces()

    # Release resources
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()