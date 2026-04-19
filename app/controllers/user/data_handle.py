

from fastapi import Depends,UploadFile, File



from app.middleware.auth_middleware import jwt_auth
from app.utils.data_preprocess import DataExtractionProcess

from ...services.user_service import UserService




from fastapi.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils.enum import userType

import json


import pandas as pd
import io

async def bussinessData(file: UploadFile = File(...),user = Depends(jwt_auth)):
    try:
        #   Validate file type
        if not file.filename.endswith((".csv", ".xlsx", ".xls",".json",".txt")):
            return JSONResponse(content={"status":400, "message": "Only CSV, JSON, TXT(JSON) and Excel files are allowed"},status_code=400)

        #   Read file content
        contents = await file.read()

        #   Convert into DataFrame
        if file.filename.endswith(".csv"):
            df = await run_in_threadpool(DataExtractionProcess.prepare_csv_data,contents)
        
        elif file.filename.endswith(".xls"):
            # df = pd.read_excel(io.BytesIO(contents), engine="xlrd")
            df = await run_in_threadpool(DataExtractionProcess.prepare_excel_old_version_data,contents)
            

        elif file.filename.endswith(".xlsx"):
            # df = pd.read_excel(io.BytesIO(contents), engine="openpyxl")
            df = await run_in_threadpool(DataExtractionProcess.prepare_excel_data,contents)
            

        #   JSON file
        elif file.filename.endswith(".json"):
            df = await run_in_threadpool(DataExtractionProcess.prepare_json_data,contents)


        #  TXT file (try parsing JSON inside it)
        elif file.filename.endswith(".txt"):
            df = await run_in_threadpool(DataExtractionProcess.prepare_txt_data,contents)
        
        else:
             return JSONResponse(content={"status":400, "message": "Unsupported file type. Allowed: CSV, Excel, JSON, TXT(JSON)"},status_code=400)
        #  Example: check data
        if df.empty:
           return JSONResponse(content={"status":400, "message": "file is empty"},status_code=400)

        #  Debug / print first rows
        print(df.head())
        data= await run_in_threadpool(DataExtractionProcess.data_ready_for_db,user.id, contents)
        

        #  Convert to JSON if needed
        # data = df.to_dict(orient="records")
        return  JSONResponse(content={
            "success": True,
            "message": "File processed successfully",
            "total_records": len(data),
            "data": data    # preview
        },status_code=200)
    except Exception as e:
       return JSONResponse(content={"status":500, "message": str(e)},status_code=500)