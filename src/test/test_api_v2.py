import io
import os
import cv2
import pytest

from typing import Generator
from numpy import dtype, generic, ndarray
from fastapi.testclient import TestClient

from main import app
from src.utils import create_image


TypeImage = Generator[ndarray[int, dtype[generic]], None, None]


class TestExtractCardNumber:
    
    client = TestClient(app)
    code = '123456789123'
    serial = "0000123456789"
    url = "/api/v2/extract-card-number"

    @pytest.fixture()
    def test_image(self) -> TypeImage:
        size = (180, 650)
        list_text = ["Serial Number:", f"{self.serial}            {self.code}"]
        file_path = "test_image.jpg"
        create_image(size, list_text, file_path)
        image = cv2.imread(file_path)
        yield image
        os.remove(file_path)


    def test_extract_card_number_with_valid_image(self, test_image: TypeImage) -> None:
        image_file = io.BytesIO(cv2.imencode(".jpg", test_image)[1]).getvalue()
        response = self.client.post(self.url, files={"image": ("test_image.jpg", image_file, "image/jpeg")})
        assert response.status_code == 200
        assert response.json().get("status") == "success"
        assert response.json().get("message") == "card number extracted successfully"
        assert response.json().get("cardNumbers")[0].get("code") == self.code
        assert response.json().get("cardNumbers")[0].get("serial") == self.serial


    def test_extract_card_number_with_invalid_image(self, test_image: TypeImage) -> None:
        response = self.client.post(self.url)
        assert response.status_code == 400
        assert response.json() == {"detail": {"status": "fail", "message": "image field is required"}}


    def test_extract_card_number_with_image_not_containing_card_number(self, test_image: TypeImage) -> None:
        size = (500, 500)
        list_text = ["Hello World", "Lorem Ipsum Dolor Sit Amet"]
        file_path = "test_image.jpg"
        create_image(size, list_text, file_path)
        image_file = io.BytesIO(cv2.imencode(".jpg", cv2.imread(file_path))[1]).getvalue()
        response = self.client.post(self.url, files={"image": ("test_image.jpg", image_file, "image/jpeg")})
        assert response.status_code == 400
        assert response.json() == {"detail": {"status": "fail", "message": "card number extraction failed"}}
