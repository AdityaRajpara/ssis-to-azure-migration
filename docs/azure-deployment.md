# Azure deployment path

1. Create resource groups and provision ADLS Gen2 (hierarchical namespace), ADF, a Spark service (Synapse Spark or Databricks), Synapse SQL as needed, Purview, Key Vault, and monitoring.
2. Create private endpoints/network rules and managed identities. Grant least-privilege data-plane roles on the lake and secret access through Key Vault.
3. Import `infra/adf/pipeline.json` into a development factory, build linked services/datasets, select the Spark activity runtime, and parameterize dev/test/prod endpoints.
4. Deploy storage containers and folder ACLs. Use date/run identifiers in paths and define retention/lifecycle policy.
5. Register sources and lake assets in Purview. Load glossary terms and lineage using supported connectors or the Purview Data Map APIs; the JSON here is an implementation-agnostic metadata example.
6. Configure the GitHub Actions or Azure Pipelines validation workflow. Add a gated release job only after environment approvals and secret federation are configured.
7. Optionally configure a Snowflake storage integration and external stage. The SQL file is a serving-layer example and requires Snowflake objects and permissions.

No credentials, cloud subscription identifiers, or live deployment resources are included. Validate the templates against current service versions and your organization's security controls before deploying.
