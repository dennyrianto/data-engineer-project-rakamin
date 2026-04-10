USE DWH;
GO

CREATE PROCEDURE BalancePerCustomer
    @name VARCHAR(255)
AS
BEGIN
    SELECT 
        c.CustomerName,
        a.AccountType,
        a.Balance,
        a.Balance + ISNULL(SUM(CASE 
                                  WHEN t.TransactionType = 'Deposit' THEN t.Amount 
                                  ELSE -t.Amount 
                               END), 0) AS CurrentBalance
    FROM DimCustomer c
    JOIN DimAccount a ON c.CustomerID = a.CustomerID
    LEFT JOIN FactTransaction t ON a.AccountID = t.AccountID
    WHERE 
        c.CustomerName LIKE '%' + @name + '%'
        AND a.Status = 'active'
    GROUP BY 
        c.CustomerName,
        a.AccountType,
        a.Balance;
END;
GO