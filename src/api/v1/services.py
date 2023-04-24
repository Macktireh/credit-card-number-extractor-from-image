import os
import cv2
import pytesseract


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"D:\application\Tesseract-OCR\tesseract.exe"
    )


class ExtarctorCardNumberFromImage:
    def __init__(self, image) -> None:
        self.image = image

    def imageToString(self) -> str | None:
        try:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            _, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
            return pytesseract.image_to_string(threshed, lang="eng", config="--psm 6")
        except Exception as e:
            print(str(e) + " Add path environment variable TESSERACT_CMD")
            return None

    def get_card_number(self, list_text: list) -> list[str | None]:
        listCardNumber = []
        for text in list_text:
            if len(text) == 12 and text.isdigit():
                listCardNumber.append(text)
            elif len(text) > 12:
                for i in text.split(' '):
                    if len(i) == 12 and i.isdigit():
                        listCardNumber.append(i)
        return listCardNumber
