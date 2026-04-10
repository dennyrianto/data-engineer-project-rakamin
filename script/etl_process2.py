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

    # ETL Untuk DimBranch
    print("\nMemulai ETL untuk DimBranch...")
    # Extract
    df_branch = pd.read_sql("SELECT * FROM branch", conn_source)
    
    # Transform (mengubah ke PascalCase)
    df_branch.columns = ['BranchID', 'BranchName', 'BranchLocation']
    
    # Load
    cursor.execute("DELETE FROM DimBranch") # Mencegah duplikasi jika script diulang
    insert_branch = "INSERT INTO DimBranch (BranchID, BranchName, BranchLocation) VALUES (?, ?, ?)"
    cursor.executemany(insert_branch, df_branch.values.tolist())
    print(f"SUCCESS! {len(df_branch)} baris data berhasil dimasukkan ke DimBranch.")


    # ETL untuk DimAccount
    print("\nMemulai ETL untuk DimAccount...")
    # Extract
    df_account = pd.read_sql("SELECT * FROM account", conn_source)
    
    # Transform (Mengubah ke PascalCase)
    df_account.columns = ['AccountID', 'CustomerID', 'AccountType', 'Balance', 'DateOpened', 'Status']
    
    # Load
    cursor.execute("DELETE FROM DimAccount") 
    insert_account = "INSERT INTO DimAccount (AccountID, CustomerID, AccountType, Balance, DateOpened, Status) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(insert_account, df_account.values.tolist())
    print(f"SUCCESS! {len(df_account)} baris data berhasil dimasukkan ke DimAccount.")

    # Menyimpan semua perubahan ke database DWH
    conn_target.commit()
    print("\nSELURUH TABEL DIMENSI TELAH BERHASIL DIISI!")

except Exception as e:
    print("Terjadi kesalahan:")
    print(e)
finally:
    if 'conn_source' in locals(): conn_source.close()
    if 'conn_target' in locals(): conn_target.close()