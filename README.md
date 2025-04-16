
# Data Ingestion Tool: Bidirectional ClickHouse & Flat File Data Ingestion Tool
This is a web-based application that facilitates bidirectional data ingestion between a ClickHouse database and Flat File (CSV) data sources. It provides an intuitive user interface for managing data ingestion, authentication via JWT tokens, and offers multiple additional features like column selection, error handling, and data preview.

## 📌 Objective

✅The goal of this project is to develop a web-based tool that facilitates bidirectional data ingestion between a ClickHouse database and a Flat File (CSV). Users can:

    - Choose the source of data (ClickHouse or Flat File).

    - Select specific columns for ingestion.

    - Ingest data efficiently in either direction.

✅The application supports JWT token authentication for ClickHouse, error handling, and provides feedback with the number of records processed.

---

## ⚙️ Features

### ✅ Core Functionality
- [x] Web UI to choose source: `ClickHouse` or `Flat File`
- [x] Flat File → ClickHouse ingestion
- [x] ClickHouse → Flat File ingestion
- [x] Support for JWT-authenticated ClickHouse connections
- [x] Schema discovery and column selection UI
- [x] Record count reporting after ingestion
- [x] Basic error handling with user-friendly messages

### ✅ UI Features
- Source/Target dropdown
- Input fields for all connection parameters
- Load Columns button
- Column selection (checkboxes)
- Start Ingestion button
- Status updates and result display

---

## 🧪 Testing & Datasets

### ✅ Test Cases Executed
1. ✅ Flat File → ClickHouse table (with column selection) → record count validated
2. ✅ ClickHouse table → Flat File → record count validated
3. ✅ ClickHouse with invalid token → Error handling validated
4. ✅ ClickHouse with invalid host → Connection error handled
5. ✅ (Optional) Preview of first 100 records implemented for both sources



### ✅ Datasets Used
- `uk_price_paid`
- `ontime` (https://clickhouse.com/docs/getting-started/example-datasets ClickHouse sample datasets)

---

## 🛠️ Tech Stack

- **Frontend**: Simple HTML, CSS, JS (form + status display)
- **Backend**: Python (FastAPI)
- **ClickHouse Client**: `clickhouse-connect` (Python client for connecting to ClickHouse)
- **CSV File Handling**: Python I/O and `csv` module
- **Authentication**: JWT token passed via ClickHouse client headers

---

## 🚀 Running the Project

### Prerequisites
- Python 3.9+
- Docker (for local ClickHouse)
- A ClickHouse instance with accessible JWT setup

### Installation

```bash
## 1. Clone the Repository
Clone the project repository to your local machine

git clone https://github.com/your-username/data-ingestion-tool
cd ingestion-tool

## 2. Install Python Dependencies
Install the required Python dependencies listed in the requirements.txt file:
pip install -r requirements.txt

## 3. Setup ClickHouse (Docker)
To set up a ClickHouse instance using Docker, run the following command:

 _> docker run -d --name clickhouse-server --ulimit nofile=262144:262144 -p 8123:8123 -p 9000:9000 clickhouse/clickhouse-server:latest

-> This will start a ClickHouse server instance and expose ports 8123 (HTTP) and 9000 (native client).

## 4. Start the Application
Run the FastAPI application:

## Backend:
Navigate to the backend folder:

cd ingestion-tool/backend

Start the FastAPI application using uvicorn:

uvicorn app:app --reload
By default, the backend will be available at http://127.0.0.1:8000


## Frontend:
If you're using VS Code, you can simply run the live server extension to view the frontend.

Alternatively, you can navigate to the frontend folder and start the frontend manually:

cd ingestion-tool/frontend


## To access the Swagger UI
-> After starting your FastAPI backend, you can access the Swagger UI to explore the available API endpoints:

-> Ensure the FastAPI backend is running: If the FastAPI backend is running (on http://127.0.0.1:8000), you should be able to view the Swagger UI directly.

-> Access the Swagger UI: After starting your FastAPI application, navigate to the following URL in your web browser:

http://127.0.0.1:8000/docs

This will open the Swagger UI interface, where you can see the available API endpoints, send test requests, and view responses.

Explore the API:

On the Swagger UI page, you will see a list of all your endpoints, including GET, POST, PUT, and other available HTTP methods.

You can interact with the API, send sample requests, and view the response directly in the Swagger interface.

FastAPI automatically generates this documentation for you, so you don't need to set anything up manually.


✨ Bonus Features (Implemented)
Multi-table JOIN in ClickHouse (supports JOIN keys and conditions).

Progress bar during ingestion to visualize the data transfer process.

Data Preview: View the first 100 records of the selected source before performing full ingestion.


📝 Additional Information
For further questions or contribution, feel free to open an issue or submit a pull request. Happy coding! 👨‍💻👩‍💻

