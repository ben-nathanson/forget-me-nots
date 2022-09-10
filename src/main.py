from fastapi import FastAPI

from src.view.routers.holiday import holiday_router

api_instance: FastAPI = FastAPI(title="Forget Me Nots")
api_instance.include_router(holiday_router)
