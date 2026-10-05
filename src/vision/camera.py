import cv2
import time

from pose_detector import create_pose_landmarker, detect_pose
from mediapipe.tasks.python.vision import PoseLandmarksConnections

def draw_landmarkers(frame, pose_landmarkers):
    #get the size of the camera frame
    height, width, _ = frame.shape

    #draw a circle for every detected body landmark
    for landmark in pose_landmarkers:
        x = int(landmark.x * width)
        y = int(landmark.y*height)

        cv2.circle(frame, (x,y), 5, (0, 255, 0), -1)

        # Connect related landmarks to create the skeleton
    for connection in PoseLandmarksConnections.POSE_LANDMARKS:
        start = pose_landmarkers[connection.start]
        end = pose_landmarkers[connection.end]

        start_x = int(start.x * width)
        start_y = int(start.y * height)

        end_x = int(end.x * width)
        end_y = int(end.y * height)

        cv2.line(
            frame,
            (start_x, start_y),
            (end_x, end_y),
            (255, 255, 255),
            2
        )


def run_camera():
    # Open the default camera 
    camera = cv2.VideoCapture(0)

    #Make sure the camera opened successfully 
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return
    
    print('Camera was opened successfully.')
    print("Press 'q' to quit the camera.")

    pose_landmarker = create_pose_landmarker()
    start_time = time.time()
    

    while True:
        # Read one frame from the camera 
        success, frame = camera.read()

        if not success:
            print("Error: Could not read the camera frame.")
            break

        #create time stamp for MediaPipe video prosesing
        timestamp_ms = int((time.time() - start_time) * 1000)

        #detect pose landmarks 
        result = detect_pose(
            pose_landmarker, 
            frame,
            timestamp_ms
        )

        #print when a pose is detected 
        if result.pose_landmarks:
            print("Pose detected!!")

            draw_landmarkers(
                frame,
                result.pose_landmarks[0]   
            )

        # Display the current frame
        cv2.imshow("MIRA Camera", frame)

        # Press q to exit 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    pose_landmarker.close()
    #Release the camera
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_camera()
