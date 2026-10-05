import cv2
import mediapipe as mp

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MODEL_PATH = "models/pose_landmarker_lite.task"

def create_pose_landmarker():
    #configure the Mediapipe model
    base_options = python.BaseOptions(
        model_asset_path =MODEL_PATH
    )

    options = vision.PoseLandmarkerOptions (
        base_options=base_options, 
        running_mode = vision.RunningMode.VIDEO
    )
    # Create and return the pose landmarker
    return vision.PoseLandmarker.create_from_options(options)

def detect_pose(pose_landmarker, frame, timestamp_ms):
    #opencv uses BGR, but Media pipe expects RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    #convert the OpemCV frame into a mediaPIpe image 
    mp_image = mp.Image(
        image_format = mp.ImageFormat.SRGB,
        data = rgb_frame
    )

    #detect body landmarks 
    result =pose_landmarker.detect_for_video(
        mp_image,
        timestamp_ms
    )
    return result


