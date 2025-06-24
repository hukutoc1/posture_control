class Points:
    def __init__(self, landmarks):
        self.landmarks = landmarks

    def __getitem__(self, index):
        return self.landmarks[index]
