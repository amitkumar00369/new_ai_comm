import os
import uuid
from fastapi import File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from src.services.commonService import CommonService
from src.validations.fileValidation import fileValidation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads","images")

async def uploadImage(file: UploadFile = File(...)):
    # print("filesssssssssss",file)
    #
    #
    #
    # # ✅ generate unique filename
    # file_ext = file.filename.split(".")[-1]
    # filename = f"{uuid.uuid4()}.{file_ext}"
    #
    #
    # file_path = os.path.join(UPLOADS_DIR, filename)
    #
    #
    # # ✅ save file
    # with open(file_path, "wb") as buffer:
    #     buffer.write(await file.read())
    #
    # # ✅ public URL
    filename = await CommonService.saveImage(file)
    file_url = f"/uploads/images/{filename}"

    return JSONResponse(
        status_code=200,
        content={
            "message": "Image uploaded successfully",
            "url": file_url
        }
    )
