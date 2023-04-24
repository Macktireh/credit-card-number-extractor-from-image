from fastapi import FastAPI

from src import api


app = FastAPI(redoc_url="/", docs_url=False)

app.include_router(api.router, prefix="/api")
