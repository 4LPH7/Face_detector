# Face Detector


This project implements a real-time human counting and face recognition system using **OpenCV** and the **face_recognition** library. The system can detect and count people in a video stream, recognize registered faces, and display their names on the screen.

---

## Features

- **Real-time Face Detection**: Detects faces in a video stream using OpenCV.
- **Face Recognition**: Recognizes registered faces and displays their names.
- **People Counting**: Counts the number of people detected in the frame.
- **Face Registration**: Allows adding new faces to the system by capturing an image and assigning a name.
- **Logging**: Logs the count of people and timestamps to a CSV file for analysis.

---

## Requirements

- Python 3.7 or higher
- OpenCV (`opencv-python`)
- `face_recognition` library
- `numpy`
- `dlib` (for face recognition)
- `Pillow` (for image processing)

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/4LPH7/Face_detector.git
   cd Face_detector
   ```

2. **Set Up a Virtual Environment** (Optional but Recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   If `dlib` installation fails, follow these steps:
   - Install **Microsoft C++ Build Tools** from [here](https://visualstudio.microsoft.com/visual-cpp-build-tools/).
   - Install CMake:
     ```bash
     pip install cmake
     ```
   - Retry installing `dlib`:
     ```bash
     pip install dlib
     ```

4. **Download Precompiled `dlib`** (Optional):
   If `dlib` installation fails, download a precompiled wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#dlib) and install it:
   ```bash
   pip install path_to_downloaded_whl_file
   ```

---

## Usage

1. **Prepare Known Faces**:
   - Place images of known individuals in the `known_faces` directory.
   - Name the files as `<person_name>.jpg` (e.g., `john.jpg`).

2. **Run the Program**:
   ```bash
   python main.py
   ```

3. **Controls**:
   - **Press 'q'**: Quit the application.
   - **Press 'a'**: Add a new face. The system will capture the current frame and prompt you to enter a name.
   - **Press 's'**: Save the current count and timestamp to the log file (`logs/count_log.csv`).

4. **View Logs**:
   - The count and timestamp are saved in `logs/count_log.csv`.

---

## Project Structure

```
human-counting-face-recognition/
├── known_faces/           # Directory to store known face images
├── logs/                  # Directory to store count logs
├── main.py                # Main application file
├── face_processor.py      # Face detection and recognition module
├── counter.py             # People counting module
├── utils.py               # Utility functions
├── requirements.txt       # List of dependencies
└── README.md              # Project documentation
```

---

## Example

1. Add a known face:
   - Place an image of a person in the `known_faces` directory (e.g., `john.jpg`).
   - Run the program, and the system will recognize the person as "John".

2. Add a new face:
   - Press 'a' to capture a new face and assign a name (e.g., "Alice").
   - The system will save the face image and recognize it in future frames.

3. View logs:
   - The `logs/count_log.csv` file will contain entries like:
     ```
     2024-01-01 12:34:56,3
     2024-01-01 12:35:10,2
     ```

---

## Future Enhancements

- **Movement Tracking**: Track the movement of people in the frame.
- **Multiple Camera Support**: Extend the system to work with multiple cameras.
- **Web Interface**: Create a web-based dashboard for monitoring.
- **Alert System**: Send alerts for unauthorized persons or overcrowding.
- **Crowd Density Analysis**: Analyze crowd density in real-time.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:
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

- [OpenCV](https://opencv.org/) for computer vision capabilities.
- [face_recognition](https://github.com/ageitgey/face_recognition) for face recognition.
- [dlib](http://dlib.net/) for machine learning tools.

---

## Author

- GitHub: [@4LPH7](https://github.com/4LPH7)

Feel free to contribute or suggest improvements!

---
### Show your support

Give a ⭐ if you like this website!

<a href="https://buymeacoffee.com/arulartadg" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-violet.png" alt="Buy Me A Coffee" height= "60px" width= "217px" ></a>

