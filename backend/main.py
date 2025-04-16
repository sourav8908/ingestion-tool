from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
import pandas as pd

from models import IngestionRequest, IngestionResponse
from clickhouse_client import connect_clickhouse, fetch_tables, fetch_columns
from ingestion import ingest_clickhouse_to_file, ingest_file_to_clickhouse

app = FastAPI()


# ✅ Optional Welcome Route
@app.get("/")
def read_root():
    return {"message": "Welcome to the Integration Tool Backend 🚀"}


# ✅ ClickHouse Connection Request Model
class ClickHouseConnectionRequest(BaseModel):
    host: str
    port: int
    database: str
    username: str
    jwt_token: str
    secure: bool = True


# ✅ Connect to ClickHouse and Get Tables
@app.post("/connect-clickhouse")
def connect_clickhouse_endpoint(conn_data: ClickHouseConnectionRequest):
    try:
        client = connect_clickhouse(
            host=conn_data.host,
            port=conn_data.port,
            database=conn_data.database,
            username=conn_data.username,
            jwt_token=conn_data.jwt_token,
            secure=conn_data.secure
        )
        tables = fetch_tables(client)
        return {"message": "Connection successful", "tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Get Columns for a Specific Table from ClickHouse
@app.post("/get-columns")
def get_columns_endpoint(
    conn_data: ClickHouseConnectionRequest = Body(...),
    table_name: str = Body(...)
):
    try:
        client = connect_clickhouse(
            host=conn_data.host,
            port=conn_data.port,
            database=conn_data.database,
            username=conn_data.username,
            jwt_token=conn_data.jwt_token,
            secure=conn_data.secure
        )
        columns = fetch_columns(client, table_name)
        return {"columns": columns}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Ingest ClickHouse → File
@app.post("/ingest/clickhouse-to-file")
async def clickhouse_to_file(request: IngestionRequest):
    return await ingest_clickhouse_to_file(request)


# ✅ Ingest File → ClickHouse
@app.post("/ingest/file-to-clickhouse")
async def file_to_clickhouse(request: IngestionRequest):
    return await ingest_file_to_clickhouse(request)


# ✅ NEW: Get Columns from Flat File (CSV)
@app.get("/get_columns")
def get_columns_from_file(file_path: str, delimiter: str = ","):
    try:
        df = pd.read_csv(file_path, delimiter=delimiter)
        return {"columns": list(df.columns)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")
