import os
import datetime


def save_statistics(count, log_file="logs/count_log.csv"):
    """Save count statistics to a CSV file."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    with open(log_file, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp},{count}\n")