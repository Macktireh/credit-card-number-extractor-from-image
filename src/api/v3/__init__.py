import cv2
import numpy as np

from fastapi import APIRouter, HTTPException, UploadFile, status

from src.api.v3.schemas import Response, ResponseError, responseSchema
from src.api.v3.services import ExtarctorCardNumberFromImage


router = APIRouter()


@router.post("/extract-card-number", responses=responseSchema)
async def extract_card_number_v3(image: UploadFile | None = None) -> Response:
    if image is None:
        res = ResponseError(message="image field is required")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.dict())

    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    extractor = ExtarctorCardNumberFromImage(img)
    text = extractor.imageToString()

    listCardNumbers = extractor.get_card_number(text.split())
    try:
        pass
    except Exception as e:
        res  = ResponseError(message="something went wrong")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.dict())

    if not listCardNumbers:
        res = ResponseError(message="card number extraction failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.dict())

    return Response(cardNumbers=listCardNumbers)
