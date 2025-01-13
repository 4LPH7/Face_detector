class PeopleCounter:
    """
    Handles people detection and counting.
    """

    def __init__(self):
        self.count = 0

    def update_count(self, detections):
        """Update people count based on new detections."""
        self.count = len(detections)
        return self.count