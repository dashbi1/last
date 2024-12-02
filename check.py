# -*- coding: utf-8 -*-


import os
p0=r'C:\Users\n\Desktop\visiontest\task3\src';

imgs_folder = "imgs"  
labs_folder = "labs"  


imgs_folder=os.path.join(p0,imgs_folder);
labs_folder=os.path.join(p0,labs_folder);

# 获取 labs 文件夹中的所有 txt 文件
txt_files = [f for f in os.listdir(labs_folder) if f.endswith('.txt')]

# 遍历所有 txt 文件
for txt_file in txt_files:
    txt_path = os.path.join(labs_folder, txt_file)
    
    # 检查标签文件是否为空
    with open(txt_path, 'r') as file:
        lines = file.readlines()
    
    # 如果标签文件为空，则删除相应的图片和 txt 文件
    if len(lines) == 0:
        image_file = txt_file.replace('.txt', '.png')  # 假设图片是 .jpg 格式
        image_path = os.path.join(imgs_folder, image_file)
        
        # 删除对应的图片和 txt 文件
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted image: {image_path}")
        
        os.remove(txt_path)
        print(f"Deleted label: {txt_path}")

print("Cleanup completed!")

