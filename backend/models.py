# backend/models.py

from pydantic import BaseModel
from typing import List, Optional

class ClickHouseConfig(BaseModel):
    host: str
    port: int
    database: str
    user: str
    jwt_token: str

class FlatFileConfig(BaseModel):
    file_path: str
    delimiter: str = ','

class IngestionRequest(BaseModel):
    source_type: str  # "clickhouse" or "flatfile"
    target_type: str  # "clickhouse" or "flatfile"
    clickhouse_config: Optional[ClickHouseConfig] = None
    flatfile_config: Optional[FlatFileConfig] = None
    table_name: Optional[str] = None
    selected_columns: Optional[List[str]] = None
    join_tables: Optional[List[str]] = None  # For bonus JOIN feature
    join_conditions: Optional[str] = None

class IngestionResponse(BaseModel):
    status: str
    message: Optional[str] = None
    records_processed: Optional[int] = None
