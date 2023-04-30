FROM python:3.10 as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt update && apt install --no-install-recommends -y && apt-get install tesseract-ocr -y \
    build-essential \
    libgl1-mesa-glx \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0"]