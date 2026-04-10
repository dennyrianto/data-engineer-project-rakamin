# Designing a Data Warehouse and Implementing Stored Procedures ID/X Partners Final Task

## Project Overview
This project focuses on building a centralized Data Warehouse for a banking client to resolve reporting delays caused by fragmented data sources. The solution includes designing a Star Schema database, developing a programmatic ETL pipeline using Python, and automating business reports via SQL Stored Procedures.

## Tech Stack
* **Database:** Microsoft SQL Server
* **Language:** Python 3.x
* **Libraries:** Pandas, pyodbc, openpyxl
* **Interface:** SQL Server Management Studio (SSMS)

## Key Features
1. **Automated ETL Pipeline:** Replaced traditional GUI tools with a Python-based approach to extract data from SQL Server, CSV, and Excel formats.
2. **Data Deduplication:** Integrated a robust cleaning process that consolidated 29 raw transaction records into 25 unique, valid entries.
3. **Advanced SQL Automation:** Created Stored Procedures for dynamic reporting, including daily transaction summaries and real-time customer balance calculations.

## How to Run
1. Restore the provided `sample.bak` to your SQL Server instance.
2. Run the SQL scripts in the `/sql` folder to set up the `DWH` database and tables.
3. Update the `INSERT_SERVER_NAME_HERE` in the Python scripts.
4. Execute the Python scripts in the following order: `DimCustomer` -> `DimOthers` -> `FactTransaction`.