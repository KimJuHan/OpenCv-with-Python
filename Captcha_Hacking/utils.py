import re
import cv2
import numpy as np

RED = 0
BLUE = 1
GREEN = 2

# 같은 색의 문자를 추출 => 흑백이미지로 변환하여 반환
# image.shape => ( 높이, 너비, 3(RGB) )
def get_chars(image, color):
    other_color_1 = (color+1)%3
    other_color_2 = (color+2)%3

    # 다른 색 검정으로 칠하기
    filter = image[:, :, other_color_1] == 255
    image[filter] = [0, 0, 0]
    filter = image[:, :, other_color_2] == 255
    image[filter] = [0, 0, 0]

    # 겹치는 부분 검정색으로 만들기
    filter = image[:, :, color] < 170
    image[filter] = [0, 0, 0]

    # 겹치는 부분 제외하고 흰색으로 칠하기
    filter = image[:, :, color] != 0
    image[filter] = [255, 255, 255]

    return image

# 순서를 지키면서 이미지로부터 글자를 추출
def extract_chars(image):
    chars=[]
    colors = [RED, GREEN, BLUE]

    for color in colors:
        # 계속 실수한 부분 : image.copy()를 해줘야한다.
        # 그렇지 않으면, 계속 같은 이미지에 대하여 처리를 해주게 되어 원하는 결과가 나오지 않는다.
        image_from_one_color = get_chars(image.copy(), color)
        gray_image = cv2.cvtColor(image_from_one_color, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
        _, contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 50:
                x, y, width, height = cv2.boundingRect(contour)
                roi = gray_image[y:y+height, x:x+width]
                chars.append((x, roi))

    chars = sorted(chars, key=lambda char: char[0])

    return chars

def resize20(image):
    resized = cv2.resize(image, (20, 20))
    return resized.reshape(-1, 400).astype(np.float32)

def lstrip_0(string):
    temp = []
    for i in string:
        if i == '+' or i == '-' or i == '*':
            temp.append(i)
    splited_str = re.split('\*|\+|-', string)

    i = 0
    temp_count = 0
    result = ""
    for a in splited_str:
        a = a.lstrip('0')
        print(a, end=' ')
        if a == '':
            a = '0'
        result += a

        if i < len(splited_str) - 1:
            result += temp[temp_count]
            temp_count += 1
        i += 1

    return result






