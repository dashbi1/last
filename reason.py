
import cv2
from ultralytics import YOLO


# Load the trained model
model = YOLO('runs/detect/train3/weights/best.pt')  # Use the best weights generated after training

# Open the video file
video_path = r'C:\Users\n\Desktop\visiontest\test\output_1.mp4'  # Replace with your video path
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video frame rate and dimensions
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#print(f"Video Resolution: {frame_width}x{frame_height}, FPS: {fps}")

while True:
    # Read each frame
    ret, frame = cap.read()
    if not ret:
        break  # Exit loop if no more frames are available

    # Resize the frame to 640x480 (Width 640, Height 480)
    frame_resized = cv2.resize(frame, (640, 480))

    # Perform inference using the YOLOv8 model
    results = model(frame_resized)

    # Get inference results
    # Bounding box coordinates are usually stored in 'boxes'
    boxes = results[0].boxes.xyxy  # Get the detection boxes in xyxy format
    #print(f"Detected Boxes (xyxy): {boxes}")

    # Get the class IDs for the detected boxes
    class_ids = results[0].boxes.cls
    #print(f"Detected Class IDs: {class_ids}")

    # Get the confidence scores for the detections
    confidences = results[0].boxes.conf
    #print(f"Confidence Scores: {confidences}")

    # Extract each detection box and decode the QR code
    for box, class_id, confidence in zip(boxes, class_ids, confidences):
        x1, y1, x2, y2 = box.int().tolist()  # Get the top-left and bottom-right coordinates and convert to integers

        # Crop the QR code region from the frame
        qr_code_region = frame_resized[y1:y2, x1:x2]

        # Convert the cropped QR code region to RGB for decoding
        qr_code_image = cv2.cvtColor(qr_code_region, cv2.COLOR_BGR2RGB)



        # Draw a rectangle around the detected QR code
        cv2.rectangle(frame_resized, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green rectangle
        if class_id==0:
            str_class="CloseWise"
        else:
            str_class="AntiCloseWise"
        cv2.putText(frame_resized, str_class, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the inference results on the frame
    cv2.imshow('QR Code Detection', frame_resized)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
