FROM python:3.10 as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt update && apt install --no-install-recommends -y && apt-get install libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn -y \
    build-essential \
    libpq-dev \
    bzip2 \
    g++ \
    git \
    graphviz \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin \
    wget \
    python3-tk \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

ADD . /app
RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "main:app", "--host", "0.0.0.0"]