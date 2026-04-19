
import pandas as pd
import io
import json
from fastapi.responses import JSONResponse

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
    def data_ready_for_db(tenantId, df):
        
        data = df.to_dict(orient="records")
        for col in data:
            col["tenantId"] = tenantId

    
DataExtractionProcess = dataExtractionProcess()