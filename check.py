# -*- coding: utf-8 -*-


import os
p0=r'C:\Users\n\Desktop\visiontest\task3\src';

imgs_folder = "imgs"  
labs_folder = "labs"  


imgs_folder=os.path.join(p0,imgs_folder);
labs_folder=os.path.join(p0,labs_folder);

# ��ȡ labs �ļ����е����� txt �ļ�
txt_files = [f for f in os.listdir(labs_folder) if f.endswith('.txt')]

# �������� txt �ļ�
for txt_file in txt_files:
    txt_path = os.path.join(labs_folder, txt_file)
    
    # ����ǩ�ļ��Ƿ�Ϊ��
    with open(txt_path, 'r') as file:
        lines = file.readlines()
    
    # �����ǩ�ļ�Ϊ�գ���ɾ����Ӧ��ͼƬ�� txt �ļ�
    if len(lines) == 0:
        image_file = txt_file.replace('.txt', '.png')  # ����ͼƬ�� .jpg ��ʽ
        image_path = os.path.join(imgs_folder, image_file)
        
        # ɾ����Ӧ��ͼƬ�� txt �ļ�
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted image: {image_path}")
        
        os.remove(txt_path)
        print(f"Deleted label: {txt_path}")

print("Cleanup completed!")

