import csv
import os
import io
from fastapi.responses import JSONResponse
from clickhouse_client import connect_clickhouse, fetch_data_from_table
from models import IngestionRequest, IngestionResponse

# ✅ Ingest from ClickHouse → Flat File
async def ingest_clickhouse_to_file(ingestion_request: IngestionRequest):
    try:
        # 1. Connect to ClickHouse (single connection)
        ch_conf = ingestion_request.clickhouse_config
        client = connect_clickhouse(
            host=ch_conf.host,
            port=ch_conf.port,
            database=ch_conf.database,
            username=ch_conf.user,
            jwt_token=ch_conf.jwt_token,
            secure=False
        )

        # 2. Fetch data from the table
        table = ingestion_request.table_name
        data = fetch_data_from_table(client, table)

        # 3. Fetch column headers
        columns = ingestion_request.selected_columns or []
        if not columns:
            columns = [col for col in client.query(f"DESCRIBE TABLE {table}").result_rows]
            columns = [col[0] for col in columns]  # Only column names

        # 4. Write data to a file
        file_path = ingestion_request.flatfile_config.file_path
        delimiter = ingestion_request.flatfile_config.delimiter

        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=delimiter)
            writer.writerow(columns)  # Write headers
            writer.writerows(data)    # Write data rows

        return IngestionResponse(status="success", message=f"Data exported to {file_path}", records_processed=len(data))

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})


# ✅ Ingest from Flat File → ClickHouse
async def ingest_file_to_clickhouse(ingestion_request: IngestionRequest):
    try:
        ch_conf = ingestion_request.clickhouse_config
        file_conf = ingestion_request.flatfile_config

        # 1. Connect to ClickHouse
        client = connect_clickhouse(
            host=ch_conf.host,
            port=ch_conf.port,
            database=ch_conf.database,
            username=ch_conf.user,
            jwt_token=ch_conf.jwt_token,
            secure=False
        )

        # 2. Read file
        file_path = file_conf.file_path
        delimiter = file_conf.delimiter

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=delimiter)
            headers = next(reader)
            rows = list(reader)

        # 3. Convert to CSV string
        csv_buffer = io.StringIO()
        writer = csv.writer(csv_buffer)
        writer.writerows(rows)
        csv_data = csv_buffer.getvalue()

        # 4. Insert data using ClickHouse's CSV format
        table = ingestion_request.table_name
        query = f"INSERT INTO {table} ({', '.join(headers)}) FORMAT CSV"
        client.command(query, data=csv_data)

        return IngestionResponse(status="success", message=f"Data inserted into {table}", records_processed=len(rows))

    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})
