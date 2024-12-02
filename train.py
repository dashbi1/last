from ultralytics import YOLO


def main():
    model = YOLO('yolov8n.pt')  
    model.train(data='dataset.yaml', epochs=50, imgsz=(480,640),batch=32)

if __name__=='__main__':
    main();
