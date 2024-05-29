import time
from typing import List
from fastapi import FastAPI, Request
import uuid
from random import randrange
from datetime import datetime
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import random
from config import *
from routers.admin.admin import router as admin
from routers.main.router import router as main
import uvicorn

app = FastAPI(title="Monteia")
app.include_router(main)
app.include_router(admin)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=5000, log_level="info")