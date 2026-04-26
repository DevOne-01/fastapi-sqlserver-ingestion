CREATE DATABASE ProductIngestionDB;
GO

USE ProductIngestionDB;
GO

CREATE SCHEMA [raw];
GO

CREATE SCHEMA curated;
GO

CREATE SCHEMA [audit];
GO

CREATE TABLE [raw].products_staging(
	staging_id INT IDENTITY(1,1) PRIMARY KEY,
	[name] VARCHAR(100) NOT NULL,
	price DECIMAL(10,2) NOT NULL,
	category VARCHAR(100) NOT NULL,
    source_system VARCHAR(100) NULL,
    batch_id VARCHAR(100) NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME()
);
GO

CREATE TABLE curated.products (
    product_id INT IDENTITY(1,1) PRIMARY KEY,
    [name] VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(100) NOT NULL,
    created_at DATETIME2 DEFAULT SYSDATETIME(),
    updated_at DATETIME2 NULL
);
GO

CREATE TABLE audit.api_logs (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    request_id VARCHAR(100),
    [endpoint] VARCHAR(255),
    method VARCHAR(20),
    status_code INT,
    [message] VARCHAR(1000),
    created_at DATETIME2 DEFAULT SYSDATETIME()
);
GO

CREATE OR ALTER PROCEDURE curated.usp_load_products
AS
BEGIN
    SET NOCOUNT ON;

    MERGE curated.products AS target

    USING(
        SELECT [name], price, category
        FROM [raw].products_staging
    )AS source
    ON target.[name] = source.[name]
    AND target.category = source.category

    WHEN MATCHED THEN
        UPDATE SET
            target.price = source.price,
            target.updated_at = SYSDATETIME()
    WHEN NOT MATCHED THEN
        INSERT ([name], price, category)
        VALUES (source.[name], source.price, source.category);
END;
GO