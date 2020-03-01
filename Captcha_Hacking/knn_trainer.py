import os
import cv2
import numpy as np

file_names = list(range(0, 13))
train = []
train_labels = []

for file in file_names:
    path = './training_data/' + str(file) + '/'
    file_count = len(next(os.walk(path))[2])
    for i in range(1, file_count+1):
        img = cv2.imread(path + str(i) + '.png')
        print(img.shape)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(gray.shape)
        train.append(gray)
        train_labels.append(file)

x = np.array(train)
train = x[:, :].reshape(-1, 400).astype(np.float32)
train_labels = np.array(train_labels)[:, np.newaxis]

print(train.shape)
print(train_labels.shape)

np.savez('trained.npz', train=train, train_labels=train_labels)