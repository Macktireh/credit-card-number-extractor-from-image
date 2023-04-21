from pydantic import BaseModel


class Response(BaseModel):
    cardNumbers: list[str]
    status: str = "success"
    message: str = "card number extracted successfully"

    class Config:
        schema_extra = {
            "example": {
                "cardNumbers": ["123456789123", "123456789123", "123456789123"],
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
