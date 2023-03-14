import io
import os
import cv2
import pytest

from typing import Generator
from numpy import dtype, generic, ndarray
from fastapi.testclient import TestClient

from main import app
from utils import create_image


TypeImage = Generator[ndarray[int, dtype[generic]], None, None]


class TestExtractCardNumber:
    
    client = TestClient(app)
    card_num = '123456789123'

    @pytest.fixture()
    def test_image(self) -> TypeImage:
        size = (180, 650)
        list_text = ["Serial Number:", f"8520317314485            {self.card_num}"]
        file_path = "test_image.jpg"
        create_image(size, list_text, file_path)
        image = cv2.imread(file_path)
        yield image
        os.remove(file_path)


    def test_extract_card_number_with_valid_image(self, test_image: TypeImage) -> None:
        image_file = io.BytesIO(cv2.imencode(".jpg", test_image)[1]).getvalue()
        response = self.client.post("/extract-card-number", files={"image": ("test_image.jpg", image_file, "image/jpeg")})
        assert response.status_code == 200
        assert response.json() == {"cardNumbers": [f"{self.card_num}"], "status": "success", "message": "card number extracted successfully"}


    def test_extract_card_number_with_invalid_image(self, test_image: TypeImage) -> None:
        response = self.client.post("/extract-card-number")
        assert response.status_code == 400
        assert response.json() == {"detail": {"status": "fail", "message": "image field is required"}}


    def test_extract_card_number_with_image_not_containing_card_number(self, test_image: TypeImage) -> None:
        size = (500, 500)
        list_text = ["Hello World", "Lorem Ipsum Dolor Sit Amet"]
        file_path = "test_image.jpg"
        create_image(size, list_text, file_path)
        image_file = io.BytesIO(cv2.imencode(".jpg", cv2.imread(file_path))[1]).getvalue()
        response = self.client.post("/extract-card-number", files={"image": ("test_image.jpg", image_file, "image/jpeg")})
        assert response.status_code == 400
        assert response.json() == {"detail": {"status": "fail", "message": "card number extraction failed"}}
