import streamlit as st
import pandas as pd
from databricks import sql
from databricks.sdk.core import Config

# -----------------------------
# Databricks connection helper
# -----------------------------
cfg = Config()

def get_connection(http_path: str):
    server_hostname = cfg.host

    # clean hostname
    if server_hostname.startswith("https://"):
        server_hostname = server_hostname.replace("https://", "")
    elif server_hostname.startswith("http://"):
        server_hostname = server_hostname.replace("http://", "")

    return sql.connect(
        server_hostname=server_hostname,
        http_path=http_path,
        credentials_provider=lambda: cfg.authenticate,
    )

# -----------------------------
# Read table function
# -----------------------------
def read_table(table_name: str, conn):
    query = f"SELECT * FROM {table_name} LIMIT 1000"
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall_arrow().to_pandas()
    return result

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("📊 Databricks Dashboard (Streamlit App)")

http_path = st.text_input("SQL Warehouse HTTP Path")
table_name = st.text_input("Unity Catalog Table (catalog.schema.table)")

if st.button("Load Data"):
    if http_path and table_name:
        try:
            conn = get_connection(http_path)
            df = read_table(table_name, conn)

            st.success("Data loaded successfully!")
            st.dataframe(df)

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both HTTP path and table name.")
