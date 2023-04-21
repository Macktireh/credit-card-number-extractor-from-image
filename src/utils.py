import cv2
import numpy as np


def create_image(size: tuple[int, int], list_text, file_path: str) -> None:

    # Créer une image blanche de size pixels
    img = np.ones((size[0], size[1], 3), dtype=np.uint8) * 255
    font: int = cv2.FONT_HERSHEY_SIMPLEX
    font_scale: float = 0.8
    thickness: int = 2

    _y: int | None = None

    for text in list_text:
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        x = int((img.shape[1] - text_size[0]) / 2)
        y = int(img.shape[0] / 2) - int(text_size[1] / 2) if _y is None else _y + text_size[1] + 40
        _y = y

        # Ajouter le texte à l'image
        cv2.putText(img, text, (x, y), font, font_scale, (0, 0, 0), thickness)
    
    # Enregistrer l'image
    cv2.imwrite(file_path, img)
