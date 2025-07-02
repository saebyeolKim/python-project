from app.models import Base
from app.db import engine

def init_db():
    Base.metadata.create_all(bind=engine)