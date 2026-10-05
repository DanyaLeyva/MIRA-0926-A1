import cv2

def run_camera():
    # Open the default camera 
    camera = cv2.VideoCapture(0)

    #Make sure the camera opened successfully 
    if not camera.isOpened():
        print("Error: Could not open the camera.")
        return
    
    print('Camera was opened successfully.')
    print("Press 'q' to quit the camera.")


    while True:
        # Read one frame from the camera 
        success, frame = camera.read()

        if not success:
            print("Error: Could not read the camera frame.")
            break

        # Display the current frame
        cv2.imshow("MIRA Camera", frame)

        # Press q to exit 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Release the camera
    camera.release()
    cv2.destoryAllWindows()

if __name__ == "__main__":
    run_camera()
