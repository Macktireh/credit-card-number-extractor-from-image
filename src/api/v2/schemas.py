from pydantic import BaseModel

from src.types import cardNumberType


class Response(BaseModel):
    cardNumbers: list[cardNumberType]
    status: str = "success"
    message: str = "card number extracted successfully"

    class Config:
        schema_extra = {
            "example": {
                "cardNumbers": [
                    {"id": 1, "code": "123456789123", "serial": "0000567891234"},
                    {"id": 2, "code": "123456789123", "serial": "0000567891234"},
                    {"id": 3, "code": "123456789123", "serial": "0000567891234"}
                ],
                "status": "success",
                "message": "card number extracted successfully",
            },
        }


class ResponseError(BaseModel):
    status: str = "fail"
    message: str


class HTTPError(BaseModel):
    detail: ResponseError

    class Config:
        schema_extra = {
            "example": {
                "detail": {"status": "fail", "message": "card number extraction failed"}
            },
        }


responseSchema = {
    200: {"model": Response},
    400: {
        "model": HTTPError,
    },
}
