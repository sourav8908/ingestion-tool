function toggleSourceTarget() {
    const sourceType = document.getElementById("source").value;
    document.getElementById("clickhouse-config").style.display =
      sourceType === "clickhouse" ? "block" : "none";
    document.getElementById("flatfile-config").style.display =
      sourceType === "flatfile" ? "block" : "none";
  }
  
  async function loadColumns() {
    const sourceType = document.getElementById("source").value;
    const url =
      sourceType === "clickhouse" ? "/get-columns" : "/get-flatfile-columns";
  
    const requestBody =
      sourceType === "clickhouse"
        ? {
            host: document.getElementById("host").value,
            port: document.getElementById("port").value,
            database: document.getElementById("database").value,
            user: document.getElementById("user").value,
            jwt_token: document.getElementById("jwt_token").value,
          }
        : {
            file_path: document.getElementById("file-path").files[0]?.name,
            delimiter: document.getElementById("delimiter").value,
          };
  
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });
  
      const data = await response.json();
      const columnsList = document.getElementById("columns-list");
      columnsList.innerHTML = "";
  
      data.columns.forEach((column) => {
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.id = column;
        checkbox.name = "columns";
        checkbox.value = column;
  
        const label = document.createElement("label");
        label.setAttribute("for", column);
        label.innerText = column;
  
        columnsList.appendChild(checkbox);
        columnsList.appendChild(label);
        columnsList.appendChild(document.createElement("br"));
      });
    } catch (error) {
      console.error("Error loading columns:", error);
      alert("Failed to load columns.");
    }
  }
  
  async function startIngestion() {
    const sourceType = document.getElementById("source").value;
    const targetType = sourceType === "clickhouse" ? "file" : "clickhouse";
    const selectedColumns = Array.from(
      document.querySelectorAll("input[name='columns']:checked")
    ).map((cb) => cb.value);
  
    const body = {
      source_type: sourceType,
      target_type: targetType,
      table_name: "users", // default, or you can add input for user to provide
      selected_columns: selectedColumns,
      flatfile_config: {
        file_path: document.getElementById("file-path").files[0]?.name,
        delimiter: document.getElementById("delimiter").value,
      },
      clickhouse_config: {
        host: document.getElementById("host").value,
        port: document.getElementById("port").value,
        database: document.getElementById("database").value,
        user: document.getElementById("user").value,
        jwt_token: document.getElementById("jwt_token").value,
        secure: false,
      },
    };
  
    try {
      const response = await fetch(
        `/ingest/${sourceType}-to-${targetType}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        }
      );
  
      const result = await response.json();
      document.getElementById("status-text").innerText = result.status || "Done";
      document.getElementById("result").innerText = `Records processed: ${result.records_processed}`;
    } catch (error) {
      console.error("Ingestion failed:", error);
      document.getElementById("status-text").innerText = "Error";
      document.getElementById("result").innerText = "Something went wrong.";
    }
  }
  