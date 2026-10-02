# ADF deployment notes

`pipeline.json` is a compact illustrative pipeline definition. In a real factory, create linked services and datasets for each REST, SQL, and ADLS connection, replace notebook activities with your selected Spark runtime, parameterize environment-specific values, and validate the exported ARM/Bicep template in a nonproduction factory. Never commit secrets; use managed identity and Key Vault references.
