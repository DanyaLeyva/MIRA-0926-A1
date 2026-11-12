import cv2
import time
from copy import copy

from mediapipe.tasks.python.vision import PoseLandmarksConnections
from src.vision.pose_detector import create_pose_landmarker, detect_pose
from src.vision.joint_angles import calculate_angle


def draw_landmarkers(frame, pose_landmarks):
    height, width, _ = frame.shape

    visibility_threshold = 0.6

    def is_visible(landmark):
        return (
            landmark.visibility is not None
            and landmark.visibility >= visibility_threshold
            and 0 <= landmark.x <= 1
            and 0 <= landmark.y <= 1
        )

    # Landmark groups
    left_arm = {11, 13, 15, 17, 19, 21}
    right_arm = {12, 14, 16, 18, 20, 22}

    left_leg = {23, 25, 27, 29, 31}
    right_leg = {24, 26, 28, 30, 32}

    # Draw visible landmarks
    for landmark in pose_landmarks:
        if not is_visible(landmark):
            continue

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    # Draw skeleton connections
    for connection in PoseLandmarksConnections.POSE_LANDMARKS:
        start = pose_landmarks[connection.start]
        end = pose_landmarks[connection.end]

        if not is_visible(start) or not is_visible(end):
            continue

        start_x = int(start.x * width)
        start_y = int(start.y * height)

        end_x = int(end.x * width)
        end_y = int(end.y * height)

        # Choose connection color
        if connection.start in left_arm and connection.end in left_arm:
            color = (0, 255, 0)  # Green

        elif connection.start in right_arm and connection.end in right_arm:
            color = (255, 0, 0)  # Blue

        elif connection.start in left_leg and connection.end in left_leg:
            color = (0, 0, 255)  # Red

        elif connection.start in right_leg and connection.end in right_leg:
            color = (0, 165, 255)  # Orange

        else:
            color = (255, 255, 255)  # White

        cv2.line(
            frame,
            (start_x, start_y),
            (end_x, end_y),
            color,
            2,
        )


def run_camera():
    # Open the default camera
    camera = cv2.VideoCapture(0)

    # Make sure the camera opened successfully
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return

    print("Camera was opened successfully.")
    print("Press 'q' to quit the camera.")

    pose_landmarker = create_pose_landmarker()
    start_time = time.time()
    previous_landmarks = None
    smoothing_alpha = 0.4

    while True:
        # Read one frame from the camera
        success, frame = camera.read()

        if not success:
            print("Error: Could not read the camera frame.")
            break

        # create time stamp for MediaPipe video prosesing
        timestamp_ms = int((time.time() - start_time) * 1000)

        # detect pose landmarks
        result = detect_pose(pose_landmarker, frame, timestamp_ms)

        # Print when a pose is detected
        if result.pose_landmarks:
            print("Pose detected!!")

            current_landmarks = result.pose_landmarks[0]

            if previous_landmarks is None:
                previous_landmarks = [
                    (landmark.x, landmark.y) for landmark in current_landmarks
                ]

            smoothed_landmarks = []

            for i, landmark in enumerate(current_landmarks):
                prev_x, prev_y = previous_landmarks[i]

                smooth_x = smoothing_alpha * landmark.x + (1 - smoothing_alpha) * prev_x

                smooth_y = smoothing_alpha * landmark.y + (1 - smoothing_alpha) * prev_y

                smoothed_landmark = copy(landmark)
                smoothed_landmark.x = smooth_x
                smoothed_landmark.y = smooth_y

                smoothed_landmarks.append(smoothed_landmark)

            previous_landmarks = [
                (landmark.x, landmark.y) for landmark in smoothed_landmarks
            ]

            draw_landmarkers(frame, smoothed_landmarks)

            def arm_visible(shoulder, elbow, wrist):
                visibility_threshold = 0.8

                for landmark in (shoulder, elbow, wrist):
                    if landmark.visibility is None:
                        return False

                    if landmark.visibility < visibility_threshold:
                        return False

                    if not (0 <= landmark.x <= 1):
                        return False

                    if not (0 <= landmark.y <= 1):
                        return False
                return True

            # get the landmarks for the left arm
            left_shoulder = smoothed_landmarks[11]
            left_elbow = smoothed_landmarks[13]
            left_wrist = smoothed_landmarks[15]

            def arm_is_visible(shoulder, elbow, wrist):
                return all(
                    landmark.visibility is not None
                    and landmark.visibility >= 0.8
                    and 0 <= landmark.x <= 1
                    and 0 <= landmark.y <= 1
                    for landmark in [shoulder, elbow, wrist]
                )

            # Calculate the angle only when all three landmarks are visible
            if arm_is_visible(left_shoulder, left_elbow, left_wrist):
                left_elbow_angle = calculate_angle(
                    left_shoulder, left_elbow, left_wrist
                )
            else:
                left_elbow_angle = None

            # get the landmarks for the right arm
            right_shoulder = smoothed_landmarks[12]
            right_elbow = smoothed_landmarks[14]
            right_wrist = smoothed_landmarks[16]

            # Calculate the right elbow angle only when landmarks are visible
            if arm_is_visible(right_shoulder, right_elbow, right_wrist):
                right_elbow_angle = calculate_angle(
                    right_shoulder, right_elbow, right_wrist
                )
            else:
                right_elbow_angle = None

            # calculate the left elbow angle
            right_elbow_angle = calculate_angle(
                right_shoulder, right_elbow, right_wrist
            )

            # Print the angle inthe terminal
            if left_elbow_angle is not None and arm_visible(
                left_shoulder, left_elbow, left_wrist
            ):
                cv2.putText(
                    frame,
                    f"Left Elbow: {left_elbow_angle:.1f} deg",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )
                # Print the angle inthe terminal
            if right_elbow_angle is not None and arm_visible(
                right_shoulder, right_elbow, right_wrist
            ):
                cv2.putText(
                    frame,
                    f"Right Elbow: {right_elbow_angle:.1f} deg",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2,
                )

        else:
            previous_landmarks = None

        # Display the camera frame
        cv2.imshow("MIRA Camera", frame)

        # Press Q to quit
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        # Close MediaPipe and release the camera
    pose_landmarker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_camera()
