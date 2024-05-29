import os
from fastapi import FastAPI, File, Request, APIRouter, UploadFile
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid
from database.models import User
from fastapi.responses import JSONResponse


router = APIRouter(prefix = "/admin", tags=["Admin"])