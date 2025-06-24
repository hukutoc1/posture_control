class Points:
    """@brief A wrapper class for landmark points to enable indexed access.

        This class provides a simple interface to access individual landmark
        points from a collection of landmarks using index notation.
    """
    def __init__(self, landmarks):
        """@brief Initialize the Points object with landmarks.

           @param landmarks A collection of landmark points to be stored.
        """
        self.landmarks = landmarks

    def __getitem__(self, index):
        """@brief Get a landmark point by index.

           @param index The index of the desired landmark point.
           @return The landmark point at the specified index.
        """
        return self.landmarks[index]
