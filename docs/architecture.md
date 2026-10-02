# Architecture and source mapping

| Domain | Input shape | Local example | Cloud landing |
|---|---|---|---|
| Operations | REST API / CSV fixture | NYC 311 service requests | `bronze/operations/service_requests` |
| Risk | REST API / CSV fixture | FRED DGS10 yields | `bronze/risk/treasury_yield` |
| Finance | JSON API and relational rows | SEC company facts plus SQLite accounts | `bronze/finance/company_facts`, `bronze/finance/accounts` |

The offline payloads are intentionally small. A SQLite in-memory table models a relational extraction from an on-premises source; it is seeded from `accounts.csv`. Each path writes raw records before transforming. Silver normalizes types and labels; Gold computes complaint counts, account exposure by domain, and dated yields. `lake/` is a local stand-in for the ADLS Gen2 filesystem. The included ADF JSON, SQL and Purview metadata are deployment starting points and need subscription-specific linked services, identities, permissions, and runtime configuration.
