class Points:
    """A wrapper class for landmark points to enable indexed access.

        This class provides a simple interface to access individual landmark
        points from a collection of landmarks using index notation.
    """

    def __init__(self, landmarks):
        """Initialize the Points object with landmarks.

        Args:
            landmarks (list or Any): A collection of landmark points to be
            stored.
                Typically a list of MediaPipe landmark objects.
        """
        self.landmarks = landmarks

    def __getitem__(self, index):
        """Get a landmark point by index.

        Args:
            index (int): The index of the desired landmark point.

        Returns:
            Any: The landmark point at the specified index. Typically a
            MediaPipe landmark object.
    """
        return self.landmarks[index]
