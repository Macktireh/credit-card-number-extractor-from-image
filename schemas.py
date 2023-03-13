from pydantic import BaseModel


class Response(BaseModel):
    cardNumber: str
    status: str
    message: str


class HTTPError(BaseModel):
    detail: Response

    class Config:
        schema_extra = {
            "example": {"detail": {"cardNumber": "", "status": "fail", "message": "description"}},
        }


responses = {
    200: {
        "model": Response
    },
    400: {
        "model": HTTPError,
    },
}