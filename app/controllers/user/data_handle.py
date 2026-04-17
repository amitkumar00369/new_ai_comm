

from fastapi import Depends, FastAPI, Response, Request,UploadFile, File, Depends, HTTPException
from pyexpat.errors import messages
from sqlalchemy import null
from starlette import status

from app.middleware.auth_middleware import jwt_auth

from ...services.passwordService import PasswordService
from app.services.sessionService import SessionService
from ...services.user_service import UserService
from app.utils.enum import userType
from app.schemas.user_schema import SignupValidation,VerifyOtps,editProfileSchema



from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType
from app.utils.constants import generateOtp, generateUserId
from datetime import datetime, timedelta
import json


import pandas as pd
import io

async def bussinessData(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.endswith((".csv", ".xlsx", ".xls",".json",".txt")):
            return JSONResponse(content={"status":400, "message": "Only CSV, JSON, TXT(JSON) and Excel files are allowed"},status_code=400)

        # Read file content
        contents = await file.read()

        #  Convert into DataFrame
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.StringIO(contents.decode("utf-8")))
        
        elif file.filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(contents), engine="xlrd")

        elif file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")

        #  JSON file
        elif file.filename.endswith(".json"):
            data = json.loads(contents.decode("utf-8"))
            df = pd.DataFrame(data)

        #  TXT file (try parsing JSON inside it)
        elif file.filename.endswith(".txt"):
            text_data = contents.decode("utf-8").strip()

            try:
                json_data = json.loads(text_data)  # try JSON parse
                df = pd.DataFrame(json_data)
            except json.JSONDecodeError:
                return JSONResponse(content={"status":400, "message": "TXT file is not valid JSON format"},status_code=400)
        else:
             return JSONResponse(content={"status":400, "message": "Unsupported file type. Allowed: CSV, Excel, JSON, TXT(JSON)"},status_code=400)
        #  Example: check data
        if df.empty:
           return JSONResponse(content={"status":400, "message": "file is empty"},status_code=400)

        #  Debug / print first rows
        print(df.head())

        #  Convert to JSON if needed
        data = df.to_dict(orient="records")

        return  JSONResponse(content={
            "success": True,
            "message": "File processed successfully",
            "total_records": len(data),
            "data": data    # preview
        },status_code=200)

    except Exception as e:
       return JSONResponse(content={"status":500, "message": str(e)},status_code=500)