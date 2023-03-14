import cv2
import numpy as np

from fastapi import FastAPI, HTTPException, UploadFile, status

from services import ExtarctorCardNumberFromImage
from schemas import Response, ResponseError, responseSchema


app = FastAPI(redoc_url="/", docs_url=False)


@app.post("/extract-card-number", responses=responseSchema)
async def extract_card_number(image: UploadFile | None = None) -> Response:
    if image is None:
        res  = ResponseError(message="image field is required")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.dict())
    
    contents = await image.read()
    nparr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    text = ExtarctorCardNumberFromImage(img).imageToString()

    try:
        listCardNumbers = ExtarctorCardNumberFromImage.getCardNumber(text.split())
    except Exception as e:
        res  = ResponseError(message="something went wrong")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=res.dict())

    if not listCardNumbers:
        res  = ResponseError(message="card number extraction failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.dict())

    return Response(cardNumbers=listCardNumbers)
