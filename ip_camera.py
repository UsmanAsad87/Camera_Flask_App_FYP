import cv2

# rtsp_url = "http://admin:User@1234usman@192.168.137.2/video"  # Replace with your V380 camera's RTSP URL
# rtsp_url = "http://192.168.137.2/"
# Open the RTSP stream
rtsp_url = "rtsp://admin:User@1234usman@192.168.137.2:5544/h264_stream"  # Replace with your V380 camera's RTSP URL

cap = cv2.VideoCapture(rtsp_url)

# Check if the stream is opened successfully
if not cap.isOpened():
    print("Failed to open the RTSP stream.")
    exit()

while True:
    # Read frames from the stream
    ret, frame = cap.read()

    # If frame reading is successful
    if ret:
        # Display the frame
        cv2.imshow("IP Camera", frame)

    # Check for the 'q' key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close the window
cap.release()
cv2.destroyAllWindows()
