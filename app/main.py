from fastapi import FastAPI
from app import models, db
from app.routes import router

models.Base.metadata.create_all(bind=db.engine)

app = FastAPI()
app.include_router(router)