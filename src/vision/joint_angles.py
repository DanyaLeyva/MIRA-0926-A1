import math


def calculate_angle(shoulder, elbow, wrist):
    # Create vectors from the elbow to the shoulder and wrist
    vector_a = (shoulder.x - elbow.x, shoulder.y - elbow.y)

    vector_b = (wrist.x - elbow.x, wrist.y - elbow.y)

    # Calculate the dot product
    dot_product = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]

    # Calculate the length of each vector
    magnitude_a = math.hypot(*vector_a)
    magnitude_b = math.hypot(*vector_b)

    # Avoid division by zero
    if magnitude_a == 0 or magnitude_b == 0:
        return None

    # Calculate the cosine of the angle
    cosine_angle = dot_product / (magnitude_a * magnitude_b)

    # Keep the value within the valid range
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    # Convert radians to degrees
    angle = math.degrees(math.acos(cosine_angle))

    return angle
