import cv2

background = cv2.imread('../icon-classifier/data/bookmark/7.img_414212.png')
overlay = cv2.imread('dice.png')

added_image = cv2.addWeighted(background, 0.4, overlay, 0.1, 0)

cv2.imwrite('combined.png', added_image)
