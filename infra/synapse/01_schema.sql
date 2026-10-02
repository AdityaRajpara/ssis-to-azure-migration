CREATE SCHEMA curated;
GO
CREATE EXTERNAL DATA SOURCE lake_gold
WITH ( LOCATION = 'abfss://<container>@<storage-account>.dfs.core.windows.net/gold' );
GO
-- Serverless SQL example over Gold Parquet; adapt credential and format configuration.
SELECT complaint_type, COUNT_BIG(*) AS request_count
FROM OPENROWSET(BULK 'operations/service_requests/**/*.parquet', DATA_SOURCE='lake_gold', FORMAT='PARQUET') AS r
GROUP BY complaint_type;
