import pandas as pd
import pyodbc


SERVER_NAME = r'INSERT_SERVER_NAME_HERE' 
SOURCE_DB = 'sample' 
TARGET_DB = 'DWH'

conn_str_source = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={SOURCE_DB};Trusted_Connection=yes;"
conn_str_target = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER_NAME};DATABASE={TARGET_DB};Trusted_Connection=yes;"

try:
    conn_source = pyodbc.connect(conn_str_source)
    conn_target = pyodbc.connect(conn_str_target)
    cursor = conn_target.cursor()
    print("Koneksi database berhasil!")

    # Extract
    print("\nMengekstrak data dari SQL, CSV, dan Excel...")
    
    query_sql = "SELECT transaction_id, account_id, transaction_date, amount, transaction_type, branch_id FROM transaction_db"
    df_sql = pd.read_sql(query_sql, conn_source)
    print(f"   -> Data SQL: {len(df_sql)} baris")
    
    df_csv = pd.read_csv('transaction_csv.csv')
    print(f"   -> Data CSV: {len(df_csv)} baris")
    
    df_excel = pd.read_excel('transaction_excel.xlsx')
    print(f"   -> Data Excel: {len(df_excel)} baris")


    #Transform
    print("\nMenggabungkan data dan menghapus duplikat...")
    
    df_combined = pd.concat([df_sql, df_csv, df_excel], ignore_index=True)
    print(f"   -> Total sebelum dibersihkan: {len(df_combined)} baris")
    
    df_combined.columns = ['TransactionID', 'AccountID', 'TransactionDate', 'Amount', 'TransactionType', 'BranchID']
    
    df_final = df_combined.drop_duplicates(subset=['TransactionID'], keep='first').copy()
    print(f"   -> Total setelah dibersihkan: {len(df_final)} baris unik yang siap dimuat")
    
    df_final['TransactionDate'] = pd.to_datetime(df_final['TransactionDate']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # Load 
    print("\nMemulai proses Load ke tabel FactTransaction...")
    
    cursor.execute("DELETE FROM FactTransaction") 
    
    insert_fact = """
        INSERT INTO FactTransaction (TransactionID, AccountID, TransactionDate, Amount, TransactionType, BranchID) 
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    cursor.executemany(insert_fact, df_final.values.tolist())
    conn_target.commit()
    
    print(f"SUCCESS! {len(df_final)} baris data berhasil dimasukkan ke FactTransaction.")
    print("SELURUH PROSES ETL TELAH SELESAI!")

except Exception as e:
    print("Terjadi kesalahan:")
    print(e)
finally:
    if 'conn_source' in locals(): conn_source.close()
    if 'conn_target' in locals(): conn_target.close()