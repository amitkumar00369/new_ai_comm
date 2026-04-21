
from fastapi import HTTPException
import pandas as pd
import io
import json
from fastapi.responses import JSONResponse
from app.utils.enum import bussinesType

from app.services.tenant_service import TenatService

class dataExtractionProcess:

    @staticmethod
    def prepare_json_data(data):
        data = json.loads(data.decode("utf-8"))
        df = pd.DataFrame(data)
        return df
    
    @staticmethod
    def prepare_csv_data(data):
        df = pd.read_csv(io.StringIO(data.decode("utf-8")))
        return df
    
    @staticmethod
    def prepare_excel_data(data):
        df = pd.read_excel(io.BytesIO(data), engine="openpyxl")
        return df
    
    @staticmethod
    def prepare_excel_old_version_data(data):
        df = pd.read_excel(io.BytesIO(data), engine="xlrd")
        return df
    @staticmethod
    def prepare_txt_data(data):
        text_data = data.decode("utf-8").strip()

        try:
            json_data = json.loads(text_data)  # try JSON parse
            df = pd.DataFrame(json_data)
            return df
        except json.JSONDecodeError:
            return JSONResponse(content={"status":400, "message": "TXT file is not valid JSON format"},status_code=400)
    @staticmethod
    def data_ready_for_db(userId, df):
        tenant = TenatService.findByUserid(userId)
        print("tenat",tenant)
        if tenant is None:
            raise HTTPException(status_code=404,detail="Tenant not found")
        createData = []
        print("type of df",type(df))

        data = df.to_dict(orient="records")

        for row in data:

            # common fields (same for all)
            base_data = {
                "tenant_id": tenant.get("id"),
                "user_id": userId,
                "title": row.get("title"),
                "price": row.get("price"),
                "location": row.get("location"),
            }

            extra_data = {}

            #  dynamic logic based on business type
            if tenant.get("business_name") == bussinesType.salon:
                extra_data = {
                    "salonType": row.get("salonType"),
                    "timing": row.get("timing"),
                    "unisex": str(row.get("unisex")).lower() in ["true", "1", "yes"]
                }

            elif tenant.get("business_name") == bussinesType.real_estate:
                extra_data = {
                    "bhk": row.get("bhk"),
                    "area": row.get("area"),
                    "furnished": row.get("furnished"),
                }

            elif tenant.get("business_name") == bussinesType.restaurants:
                extra_data = {
                    "foodType": row.get("foodType"),
                    "rating": row.get("rating"),
                    "deliveryTime": row.get("deliveryTime"),
                }

            elif tenant.get("business_name") == bussinesType.healthcare:
                extra_data = {
                    "doctorType": row.get("doctorType"),
                    "experience": row.get("experience"),
                }

            # fallback (very important)
            else:
                # store all unknown fields dynamically
                extra_data = {
                    k: v for k, v in row.items()
                    if k not in ["title", "price", "location"]
                }

            base_data["meta_data"] = extra_data
            createData.append(base_data)
            print("created",createData)
            # col["tenant_id"] = tenant.get("id")
            # col["user_id"] = userId
            # col[""]
        return createData
        

    
DataExtractionProcess = dataExtractionProcess()