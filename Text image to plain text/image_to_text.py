import os
from PIL import Image
from pytesseract import pytesseract

pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
folder_path = r'D:\python\image to text\images'
dir_list = os.listdir(folder_path)
print(dir_list)

for file in dir_list:
    file = f'{folder_path}\{file}'
    with open(file, 'r') as f:
        img = Image.open(file)
        try:
            txt = pytesseract.image_to_string(img, timeout=len(dir_list))
            print(txt)
            with open('output.txt', 'w') as f:
                f.write(txt)
        except RuntimeError as e:
            print(e)
