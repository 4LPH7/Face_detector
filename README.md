
---

# Face Recognition System

A real-time face recognition system built using OpenCV, Tkinter, and Python. This system can detect and recognize multiple faces in a video stream, register new faces, and maintain an attendance log. It is designed for ease of use and extensibility.

---

## Features

- **Real-Time Face Detection**: Detects multiple faces in a live video stream.
- **Face Recognition**: Recognizes registered faces and labels them in real-time.
- **Attendance Tracking**: Automatically logs the first and last seen timestamps for recognized faces.
- **Database Management**: Add, delete, and manage registered faces.
- **Export Attendance**: Export attendance logs to a CSV file.
- **Customizable Settings**: Adjust recognition tolerance and confidence thresholds.
- **User-Friendly GUI**: Built with Tkinter for easy interaction.

---

## Requirements

- Python 3.7+
- OpenCV (`opencv-python`)
- Pillow (`PIL`)
- NumPy (`numpy`)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/face-recognition-system.git
   cd face-recognition-system
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download Model Files**:
   - Download the following files and place them in the project directory:
     - [deploy.prototxt](https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt)
     - [res10_300x300_ssd_iter_140000_fp16.caffemodel](https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20180205_fp16/res10_300x300_ssd_iter_140000_fp16.caffemodel)

4. **Run the Application**:
   ```bash
   python face_recognition_system.py
   ```

---

## Usage

### Main Interface
- **Live Video Feed**: Displays the live video stream with detected faces.
- **Capture Faces**: Click to capture and register new faces.
- **Manage Database**: View and delete registered faces.
- **Export Attendance**: Export the attendance log to a CSV file.
- **Settings**: Adjust recognition tolerance and confidence thresholds.
- **Quit**: Exit the application.

### Registering a New Face
1. Click the **Capture Faces** button.
2. Enter the name of the detected face when prompted.
3. The system will save the face and add it to the database.

### Managing the Database
1. Click the **Manage Database** button.
2. Select a name from the list and click **Delete Selected** to remove it.

### Exporting Attendance
1. Click the **Export Attendance** button.
2. The attendance log will be saved to `attendance.csv`.

---

## File Structure

```
face-recognition-system/
├── known_faces/               # Directory for registered face images
├── face_encodings.pkl         # Database of face encodings
├── deploy.prototxt            # Face detection model configuration
├── res10_300x300_ssd_iter_140000_fp16.caffemodel  # Face detection model weights
├── face_recognition_system.py # Main application script
└── attendance.csv             # Attendance log
```

---

## Customization

### Adjusting Recognition Parameters
- **Recognition Tolerance**: Lower values make recognition stricter.
- **Confidence Threshold**: Adjust the minimum confidence for face detection.

### Adding New Features
- **Deep Learning Models**: Replace the LBP-based recognition with a deep learning model for better accuracy.
- **Network Camera Support**: Modify the video capture to work with IP cameras.
- **Advanced Anti-Spoofing**: Add liveness detection to prevent spoofing.

---

## Troubleshooting

### Common Issues
1. **Missing Model Files**:
   - Ensure `deploy.prototxt` and `res10_300x300_ssd_iter_140000_fp16.caffemodel` are in the project directory.

2. **GUI Not Displaying**:
   - Ensure OpenCV is installed with GUI support (`opencv-python`, not `opencv-python-headless`).

3. **Face Recognition Errors**:
   - Ensure faces are well-lit and clearly visible.
   - Adjust the recognition tolerance and confidence thresholds in the settings.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- OpenCV for providing the face detection models.
- Tkinter for the GUI framework.
- Python for making it all possible.

---


## Author

- GitHub: [@4LPH7](https://github.com/4LPH7)

Feel free to contribute or suggest improvements!
Let me know if you need further customization or additional sections!

---
### Show your support

Give a ⭐ if you like this website!

<a href="https://buymeacoffee.com/arulartadg" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" height= "60px" width= "217px" ></a>

