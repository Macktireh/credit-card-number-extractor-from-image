import cv2
import numpy as np

from fastapi import FastAPI, HTTPException, UploadFile, status

from api import ExtarctorCardNumberFromImage
from schemas import Response, responses


app = FastAPI(redoc_url="/", docs_url=False)


@app.post("/extract-card-number", responses=responses)
async def extract_card_number(image: UploadFile | None = None) -> Response:
    if image is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="image field is required")
    
    contents = await image.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    text = ExtarctorCardNumberFromImage(img).imageToString()

    try:
        card_number = ExtarctorCardNumberFromImage.getCardNumber(text.split())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="something went wrong")

    if not card_number:
        res  = Response(cardNumber="", status="fail", message="card number extraction failed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=res.dict())

    return Response(
        cardNumber=card_number,
        status="success",
        message="card number extracted successfully"
    )
