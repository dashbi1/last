# -*- coding: utf-8 -*-
import cv2

# ��ȡͼ��
path=r'C:\Users\n\Desktop\visiontest\test\20241026_225305_0.mp4'
cap=cv2.VideoCapture(path);
while 1:
    ret, image = cap.read()
    if not ret:
        break  # Exit loop if no more frames are available


    # ������ά������
    detector = cv2.QRCodeDetector()

    # ��Ⲣ�����ά��
    value, points, _ = detector.detectAndDecode(image)
    #cv2.imshow('aaa',image);
    # �����⵽��ά��
    if points is not None:
        # ���������
        #print("Decoded text:", value)

        # ��ͼ���ϻ��ƶ�ά����ĸ��ǵ�
        points = points.astype(int)
        #print(points);
        for i in range(4):
            top_left = tuple(points[0][0])
            bottom_right = tuple(points[0][2])  # �Խ��ߵ���һ����
            cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 3)  # ���ƾ��ο�

            
            
            x, y = points[0][0]
            text_position = (x + 10, y-20)
            cv2.putText(image, value, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # ��ʾ���
        cv2.imshow("QR Code Detection", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break;
    else:
        #print("QR Code not detected")
        pass