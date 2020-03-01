import numpy as np
import cv2
import utils
import requests
import shutil
import time

FILE_NAME = 'trained.npz'

# 각 글자의 ( 1 X 400 ) 데이터와 정답 (0 ~ 9, +, -, *)
with np.load(FILE_NAME) as data:
    train = data['train']
    train_labels = data['train_labels']
    knn = cv2.ml.KNearest_create()
    knn.train(train, cv2.ml.ROW_SAMPLE, train_labels)

def check(test, train, train_labels):
    ret, result, neighbours, dist = knn.findNearest(test, k=1)
    return result

def get_result(file_name):
    image = cv2.imread(file_name)
    chars = utils.extract_chars(image)
    result_strings = ""
    for char in chars:
        matched = check(utils.resize20(char[1]), train, train_labels)
        if matched < 10:
            result_strings += str(int(matched))
            continue
        if matched == 10:
            matched = '+'
        elif matched == 11:
            matched = '-'
        elif matched == 12:
            matched = '*'
        result_strings += matched

    return result_strings

test_str = get_result('./target_images/14.png')
print(test_str)
processed_str = utils.lstrip_0(test_str)
print(processed_str)

# host = 'http://localhost:10000'
# url = '/start'
#
# # target_images 폴더 생성
# with requests.Session() as s:
#     answer = ''
#     for i in range(0, 100):
#         start_time = time.time()
#         params = { 'ans' : answer }
#
#         # 정답을 파라미터에 담아서 전송하여, 이미지 경로를 받아오기
#         response = s.post(host+url, params)
#         if i == 0:
#             returned = response.text
#             image_url = host + returned
#             url = '/check'
#         else:
#             returned = response.json()
#             image_url = host + returned['url']
#
#         # 특정한 폴더에 이미지 파일을 업로드합니다.
#         response = s.get(image_url, stream=True)
#         target_image = './target_images/' + str(i) + '.png'
#         with open(target_image, 'wb') as f:
#             shutil.copyfileobj(response.raw, f)
#         del response
#
#         # 다운로드 받은 이미지 파일을 분석하여 답을 도출합니다.
#         answer_string = get_result(target_image)
#         answer_string = utils.lstrip_0(answer_string)
#         print(answer_string)
#         answer = str(eval(answer_string))
#
#         print('--- %s seconds ---' % (time.time() - start_time))
