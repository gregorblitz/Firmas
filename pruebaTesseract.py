import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Archivos de programa\Tesseract-OCR\tesseract'
from pytesseract import Output
from matplotlib import pyplot as plt
path_Example= 'ejemplo.jpeg'
img_color = cv2.imread(path_Example)
plt.imshow(img_color)
##plt.show()
img_gris = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
plt.imshow(img_gris)
##plt.show()
thresh_img = cv2.threshold(img_gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
plt.imshow(thresh_img)
##plt.show()
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,2))
opening_image = cv2.morphologyEx(thresh_img, cv2.MORPH_OPEN, kernel,iterations=1)
plt.imshow(opening_image)
##plt.show()
invert_image = 255 - opening_image
plt.imshow(invert_image)
plt.show()
def ocr(image):
    custom_config = r'-l spa - psm 11'
    text = pytesseract.image_to_string(image,config=custom_config )
    return text
data_image= pytesseract.image_to_data(invert_image, output_type=Output.DICT)

import re
n_boxes = len(data_image['text'])
for i in range(n_boxes):
  if int(data_image['conf'][i]) > 50:
    (x, y, w, h) = (data_image['left'][i], data_image['top'][i],data_image['width'][i], data_image['height'][i])
    img = cv2.rectangle(img_color, (x, y),(x + w, y + h),(255,0,0), 2)
plt.imshow(img)
plt.show()
cv2.imwrite('ImagenRectangulos.jpg',img)