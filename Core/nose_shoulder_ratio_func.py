from math import hypot


def nose_shoulder_ratio(points):
    """Calculate the ratio of nose-to-shoulder distance to shoulder width.

    Args:
        points (list): List of landmark points (expected to contain shoulder
                       and nose points).

    Returns:
        float or None: Ratio of vertical nose-to-shoulder distance to shoulder
                       width,or None if calculation fails due to missing
                       landmarks or invalid input.
    """
    try:
        # Left shoulder landmark point
        left_shoulder = points[11]
        # Right shoulder landmark point
        right_shoulder = points[12]
        # Nose landmark point
        nose = points[0]
        # Midpoint Y-coordinate between left and right shoulders
        mid_y = (left_shoulder.y + right_shoulder.y) / 2

        # Vertical distance from nose to shoulder midpoint
        nose_to_should = nose.y - mid_y

        # Shoulder width (Euclidean distance between left and right shoulders)
        shoulder_width = hypot(left_shoulder.x - right_shoulder.x,
                               left_shoulder.y - right_shoulder.y)

        # Avoid division by zero
        if shoulder_width == 0:
            return None

        # Return the computed ratio
        return nose_to_should / shoulder_width
    except Exception:
        return None
