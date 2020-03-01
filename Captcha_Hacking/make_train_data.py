import os
import cv2
import utils

# raw_images 디렉토리에 있는 파일들에 대하여
all_files = next(os.walk('./raw_images'))[2]
for i in all_files:
    image = cv2.imread('./raw_images/' + i)
    chars = utils.extract_chars(image)

    for char in chars:
        cv2.imshow('image', char[1])
        input = cv2.waitKey(0)

        resized = cv2.resize(char[1], (20, 20))
        if input >= 48 and input <= 57:
            name = str(input-48)
        elif input == ord('a') or input == ord('b') or input == ord('c'):
            name = str(input - ord('a') + 10)
        file_count = len(next(os.walk('./training_data/' + name))[2])
        cv2.imwrite('./training_data/' + name + '/' + str(file_count + 1) + '.png', resized)

