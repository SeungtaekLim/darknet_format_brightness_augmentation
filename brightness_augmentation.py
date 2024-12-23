import os
import shutil
import cv2
import numpy as np

# 데이터 파일 경로 설정 (이미지와 텍스트 파일이 모두 이곳에 있음)
data_dir = './data/'

# 결과 파일 경로 설정 (결과 폴더를 'result'에 저장)
result_base_dir = './result/'

# 밝기 값과 대비 값을 설정
brightness_values = [-10, 0, 10]
contrast_values = [0.5, 0.8, 1.0, 1.2, 1.5]

# 결과 디렉터리
result_dirs = {}

for brightness in brightness_values:
    for contrast in contrast_values:
        result_dir_name = f"result_brightness_{brightness}_contrast_{contrast}"
        result_dir_path = os.path.join(result_base_dir, result_dir_name)
        result_dirs[(brightness, contrast)] = result_dir_path
        
        if not os.path.exists(result_dir_path):
            os.makedirs(result_dir_path)

image_files = [f for f in os.listdir(data_dir) if f.endswith('.png') or f.endswith('.jpg')]
txt_files = [f for f in os.listdir(data_dir) if f.endswith('.txt')]

image_length = len(image_files)

for index1 in range(image_length):
    img_name_without_ext = os.path.splitext(image_files[index1])[0]

    img_path = os.path.join(data_dir, image_files[index1])

    txt_file_name = img_name_without_ext + '.txt'
    
    if txt_file_name in txt_files:
        txt_path = os.path.join(data_dir, txt_file_name)

        with open(txt_path, 'r') as file:
            lines = file.readlines()

        for brightness in brightness_values:
            img = cv2.imread(img_path)

            adjusted_img = cv2.convertScaleAbs(img, alpha=1, beta=brightness)

            for contrast in contrast_values:
                contrast_img = cv2.convertScaleAbs(adjusted_img, alpha=contrast, beta=0)

                result_dir = result_dirs[(brightness, contrast)]

                result_img_name = f"qfn_{index1 + 1}_brightness_{brightness}_contrast_{contrast}.png"
                
                cv2.imwrite(os.path.join(result_dir, result_img_name), contrast_img)

                result_txt_name = f"qfn_{index1 + 1}_brightness_{brightness}_contrast_{contrast}.txt"

                with open(os.path.join(result_dir, result_txt_name), 'w') as new_file:
                    for line in lines:
                        parts = line.split()

                        class_id = parts[0]
                        center_x_norm = float(parts[1])
                        center_y_norm = float(parts[2])
                        width_norm = float(parts[3])
                        height_norm = float(parts[4])

                        new_line = f"{class_id} {center_x_norm} {center_y_norm} {width_norm} {height_norm}\n"
                        new_file.write(new_line)

                print(f"처리 중: 이미지 {image_files[index1]}, 밝기 {brightness}, 대비 {contrast}")

    else:
        print(f"경고: 이미지 파일 {image_files[index1]}에 대응하는 텍스트 파일이 없습니다. 해당 이미지는 텍스트 파일 없이 처리됩니다.")

print("이미지 및 텍스트 파일의 밝기와 대비 조정과 복사가 완료되었습니다.")
