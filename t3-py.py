# -*- coding: utf-8 -*-
import cv2

# 读取图像
path=r'C:\Users\n\Desktop\visiontest\test\20241026_225305_0.mp4'
cap=cv2.VideoCapture(path);
while 1:
    ret, image = cap.read()
    if not ret:
        break  # Exit loop if no more frames are available


    # 创建二维码检测器
    detector = cv2.QRCodeDetector()

    # 检测并解码二维码
    value, points, _ = detector.detectAndDecode(image)
    #cv2.imshow('aaa',image);
    # 如果检测到二维码
    if points is not None:
        # 输出解码结果
        #print("Decoded text:", value)

        # 在图像上绘制二维码的四个角点
        points = points.astype(int)
        #print(points);
        for i in range(4):
            top_left = tuple(points[0][0])
            bottom_right = tuple(points[0][2])  # 对角线的另一个点
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)  # 绘制矩形框

            
            
            x, y = points[0][0]
            text_position = (x + 10, y-20)
            cv2.putText(image, value, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 显示结果
        cv2.imshow("QR Code Detection", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
    else:
        #print("QR Code not detected")
        pass