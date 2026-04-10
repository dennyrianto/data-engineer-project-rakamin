CREATE TABLE DimBranch (
    BranchID INT PRIMARY KEY,
    BranchName VARCHAR(255),
    BranchLocation VARCHAR(255)
);

CREATE TABLE DimCustomer (
    CustomerID INT PRIMARY KEY,
    CustomerName VARCHAR(255),
    Address VARCHAR(255),
    CityName VARCHAR(255),
    StateName VARCHAR(255),
    Age INT,
    Gender VARCHAR(50),
    Email VARCHAR(255)
);

CREATE TABLE DimAccount (
    AccountID INT PRIMARY KEY,
    CustomerID INT,
    AccountType VARCHAR(50),
    Balance DECIMAL(18, 2),
    DateOpened DATETIME,
    Status VARCHAR(50),
    FOREIGN KEY (CustomerID) REFERENCES DimCustomer(CustomerID)
);

CREATE TABLE FactTransaction (
    TransactionID INT PRIMARY KEY,
    AccountID INT,
    BranchID INT,
    TransactionDate DATETIME,
    Amount DECIMAL(18, 2),
    TransactionType VARCHAR(50),
    FOREIGN KEY (AccountID) REFERENCES DimAccount(AccountID),
    FOREIGN KEY (BranchID) REFERENCES DimBranch(BranchID)
);