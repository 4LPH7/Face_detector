import os
import datetime
import csv


def save_statistics(count, log_file="logs/count_log.csv"):
    """
    Save count statistics to a CSV file.

    Args:
        count (int): The current count of people.
        log_file (str): Path to the log file.
    """
    if not os.path.exists("logs"):
        os.makedirs("logs")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file_exists = os.path.isfile(log_file)
        with open(log_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            # Write header if the file is new
            if not file_exists:
                writer.writerow(["Timestamp", "Count"])
            writer.writerow([timestamp, count])
        print(f"Saved count: {count} at {timestamp}")
    except Exception as e:
        print(f"Failed to save statistics: {e}")
