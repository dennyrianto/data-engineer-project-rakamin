import pandas as pd
import pyodbc

SERVER_NAME = 'INSERT_SERVER_NAME_HERE' 

SOURCE_DB = 'sample' 
TARGET_DB = 'DWH'

conn_str_source = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={SOURCE_DB};Trusted_Connection=yes;"
conn_str_target = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={TARGET_DB};Trusted_Connection=yes;"

try:
    conn_source = pyodbc.connect(conn_str_source)
    conn_target = pyodbc.connect(conn_str_target)
    print("Koneksi database berhasil!")

    
    #Extract
    print("Memulai proses Extract...")
    query_extract = """
        SELECT 
            c.customer_id, 
            c.customer_name, 
            c.address, 
            ci.city_name, 
            s.state_name, 
            c.age, 
            c.gender, 
            c.email
        FROM customer c
        JOIN city ci ON c.city_id = ci.city_id
        JOIN state s ON ci.state_id = s.state_id
    """
    df_customer = pd.read_sql(query_extract, conn_source)

    # Transform
    print("Memulai proses Transform...")
    
    df_customer.columns = [
        'CustomerID', 'CustomerName', 'Address', 'CityName', 
        'StateName', 'Age', 'Gender', 'Email'
    ]

    # b. Mengubah huruf menjadi KAPITAL, kecuali CustomerID, Age, dan Email
    cols_to_upper = ['CustomerName', 'Address', 'CityName', 'StateName', 'Gender']
    for col in cols_to_upper:
        # Menghindari error jika ada data kosong (NaN)
        df_customer[col] = df_customer[col].str.upper().fillna('UNKNOWN')


    # PRoses Load
    print("Memulai proses Load ke tabel DimCustomer...")
    cursor = conn_target.cursor()

    cursor.execute("DELETE FROM DimCustomer")

    insert_query = """
        INSERT INTO DimCustomer (CustomerID, CustomerName, Address, CityName, StateName, Age, Gender, Email)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    records = df_customer.values.tolist()
    
    cursor.executemany(insert_query, records)
    conn_target.commit()

    print(f"SUCCESS! {len(df_customer)} baris data berhasil dimasukkan ke DimCustomer di DWH.")

except Exception as e:
    print("Terjadi kesalahan:")
    print(e)
finally:
    if 'conn_source' in locals(): conn_source.close()
    if 'conn_target' in locals(): conn_target.close()