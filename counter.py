class PeopleCounter:
    """
    Handles people detection and counting.
    """

    def __init__(self):
        self.count = 0
        self.history = []

    def update_count(self, detections):
        """
        Update people count based on new detections.

        Args:
            detections (list): List of face detections in the current frame.

        Returns:
            int: Updated count of people.
        """
        self.count = len(detections)
        self.history.append(self.count)
        return self.count

    def get_average_count(self):
        """Calculate and return the average count from the history."""
        return sum(self.history) / len(self.history) if self.history else 0

    def reset_history(self):
        """Reset the history of counts."""
        self.history = []
