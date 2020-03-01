import cv2
import utils

image = cv2.imread('./raw_images/1.png')
print(image.shape)
red = utils.get_chars(image.copy(), utils.RED)
green = utils.get_chars(image.copy(), utils.GREEN)
blue = utils.get_chars(image.copy(), utils.BLUE)
cv2.imshow('Image Gray', red)
cv2.waitKey(0)
cv2.imshow('Image Gray', green)
cv2.waitKey(0)
cv2.imshow('Image Gray', blue)
cv2.waitKey(0)


