from fastapi import FastAPI

from src.view.routers.holiday import holiday_router

app: FastAPI = FastAPI(title="Forget Me Nots")
app.include_router(holiday_router)
