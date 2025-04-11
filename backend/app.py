from fastapi import FastAPI
from csv_api.routes import router as csv_router

app = FastAPI(title="Finance CSV API")
app.include_router(csv_router, prefix="/api")
