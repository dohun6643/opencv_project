import cv2
import os

path = '/home/dohun/Documents/imageroad'
save_path = '/home/dohun/Documents/opencv_project/ImageCropped'

if not os.path.isdir(save_path):
    os.mkdir(save_path)

image_files = [f for f in os.listdir(path) if f.endswith('.jpg')]

for file in image_files:
    w = 0

    sample_image = cv2.imread(path + str(file))

    height = sample_image.shape[0]
    width = sample_image.shape[1]

    window_width = 500
    window_height = 500

    writer = file.split('.')[0]

    if not os.path.isdir(save_path + '/' + writer + '/'):
        os.mkdir(save_path + '/' + writer + '/')

    for i in range(0, height, window_height):
        for j in range(0, width, window_width):
            crop_image = sample_image[i:i+window_height, j:j+window_width]
            cv2.imwrite(save_path + '/' + writer + '/' + str(w) + '.png', crop_image)
            w = w + 1

for root, dirs, files in os.walk(save_path):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        print(len(path) * '---', file)