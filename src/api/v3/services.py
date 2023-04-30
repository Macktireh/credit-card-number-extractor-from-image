import os
import cv2
import pytesseract

from src.api.v2.services import ExtarctorCardNumberFromImage as ExtarctorCardNumberFromImageV1
from src.types import cardNumberType


if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"D:\application\Tesseract-OCR\tesseract.exe"
    )


class ExtarctorCardNumberFromImage(ExtarctorCardNumberFromImageV1):
    def __init__(self, image) -> None:
        self.image = image

    def get_card_number(self, list_text: list) -> list[cardNumberType]:
        listCardNumber = []
        for text in list_text:
            if len(text) == 12 and text.isdigit():
                listCardNumber.append(text)
            elif len(text) == 13 and text.isdigit():
                listCardNumber.append(text)
            elif len(text) > 12:
                for i in text.split(" "):
                    if len(i) == 12 and i.isdigit():
                        listCardNumber.append(i)
                    elif len(i) == 13 and i.isdigit():
                        listCardNumber.append(i)
        list_tuple = self.get_tuple_list(listCardNumber)
        return self.format_data(list_tuple)

    @staticmethod
    def get_tuple_list(input_list: list[str]) -> list[tuple[str, str]]:
        output_list = []
        while len(input_list) >= 2:
            num = input_list[0]
            index = input_list.index(num)
            input_list.pop(index)
            next_num = input_list[index]
            input_list.pop(index)
            output_list.append((num, next_num))
        return output_list

    @staticmethod
    def format_data(data_list: list[tuple[str, str]]) -> list[cardNumberType]:
        result_list = []
        for i, data_tuple in enumerate(data_list):
            value1, value2 = data_tuple
            if len(value1) == 12 and not value1.startswith("0000"):
                code = value1
                serial = value2
            else:
                code = value2
                serial = value1
            result_list.append({"id": i + 1, "code": code, "serial": serial})
        return result_list
