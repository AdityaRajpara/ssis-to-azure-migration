# Legacy SSIS to Azure Cloud Migration — Enterprise ETL Modernization

A runnable portfolio simulation of migrating a legacy SSIS-style batch workflow to an Azure-style lakehouse. The legacy path and migrated path process the same public/demo inputs and produce reconciled outputs. This repository does **not** claim access to a real enterprise SSIS estate, Azure subscription, or measured production savings.

## What it demonstrates

- API, SQLite relational, and CSV flat-file ingestion into append-oriented Bronze.
- A configuration-driven legacy package runner that models SSIS control flow, staging, and SQL transformations.
- A cloud-style path: ADF orchestration templates → ADLS Gen2-shaped medallion paths → PySpark Silver/Gold jobs → Synapse/Snowflake SQL examples.
- Validation, deterministic reconciliation, lineage metadata, and repeatable local timing/size benchmarks.
- Azure DevOps and GitHub Actions validation/deployment examples.

## Data sources

1. **NYC 311 Service Requests** (operations): Socrata API, dataset `erm2-nwe9`; the demo requests a small recent sample. [Dataset/API](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9) · [Socrata API guide](https://dev.socrata.com/docs/).
2. **FRED DGS10** (risk/economic indicator): an official Federal Reserve Bank of St. Louis series. Live API requires a free API key; this project supports it via `FRED_API_KEY`. [Series](https://fred.stlouisfed.org/series/DGS10) · [API docs](https://fred.stlouisfed.org/docs/api/fred/series_observations.html).
3. **SEC company facts** (finance): downloadable public JSON endpoint. The SEC requires a descriptive `User-Agent`; configure `SEC_USER_AGENT`. [Company Facts API](https://www.sec.gov/edgar/sec-api-documentation).

The offline demo ships deterministic synthetic fixtures under `data/flatfiles/`. SQLite is used as the relational source, populated from the bundled fixture on every fresh run. These fixtures are clearly labeled as synthetic and are not represented as downloaded public records. Use `--live` to call public endpoints; set `FRED_API_KEY` and `SEC_USER_AGENT` as needed. NYC Socrata works without an app token at modest request volume.

## Run locally

Requires Python 3.10+. No cloud account or Docker is needed.

```bash
python -m venv .venv
source .venv/bin/activate             # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -e .
python -m migration_demo.cli run --mode both
python -m migration_demo.cli reconcile
python -m migration_demo.cli benchmark --iterations 3
```

Default mode is offline and repeatable. Outputs land in `lake/` and `artifacts/`; both are ignored by Git. To fetch public data, run `python -m migration_demo.cli run --mode both --live`.

Optional PySpark execution: install `pip install -e '.[spark]'`, then run `python -m migration_demo.cli run --mode cloud --engine spark`. Local default uses equivalent Python transformations so the demo stays lightweight. The local reconciliation and two unit tests were executed successfully on the bundled fixtures. A tiny local benchmark was also executed; its raw timing report is in the ignored `artifacts/` directory and is not evidence of a production cost reduction. See [benchmarking notes](docs/benchmarking.md).

## Architecture

```text
NYC 311 REST ─┐
FRED API ──────┼─> Ingestion ─> Bronze (raw JSON/CSV) ─> Silver (typed/validated) ─> Gold marts
SEC JSON ──────┤         │                                                       ├─ Synapse SQL
CSV fixture ───┤         └─ SQLite relational source                             └─ Snowflake SQL
SQLite ────────┘
                   Legacy package run ───────────┐
                   Cloud-style run ──────────────┴─> deterministic reconciliation
```

The production target layout is `abfss://<container>@<account>.dfs.core.windows.net/{bronze,silver,gold}/<domain>/<entity>/...`. Locally, the same logical layout is represented below `lake/`.

## Repository map

- `src/migration_demo/`: ingestion, legacy package simulation, local/PySpark transformations, reconciliation, benchmark, CLI.
- `config/`: source and legacy workflow configuration.
- `data/flatfiles/`: small synthetic fixtures used for offline runs.
- `infra/adf/`: ADF pipeline and linked-service parameter examples.
- `infra/synapse/`, `infra/snowflake/`: serving layer SQL.
- `infra/purview/`: collection, glossary, and lineage examples.
- `azure-pipelines/`, `.github/workflows/`: CI examples.
- `docs/`: migration strategy, architecture, and operating guide.

## Migration controls

`reconcile` compares canonical business outputs from legacy and cloud paths by row counts, duplicate keys, null checks, and numeric totals. A pass means these two implementations agree for this input snapshot; it does not prove source completeness or production fitness. Benchmarks report wall time and output bytes for the current machine and input only. No cost saving is inferred from local timing.

## Azure deployment path

The templates are parameterized examples, not a one-click production deployment. Provision ADLS Gen2, ADF, a Spark runtime (Synapse or Databricks), Key Vault, and Purview in a subscription; configure managed identities and private networking; replace placeholders; validate linked services; then publish ADF artifacts using the included pipeline examples. Snowflake is optional and requires separately configured credentials. See [migration guide](docs/migration-guide.md) and [Azure deployment](docs/azure-deployment.md).

## GitHub push

Create an empty repository on GitHub under your account, then from this directory:

```bash
git init -b main
git add .
git commit -m "Build SSIS to Azure migration simulation"
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPOSITORY>.git
git push -u origin main
```

If this folder already has a Git repository, use `git status` first and do not reinitialize it. Replace both placeholders with the repository you create. No repository was created or pushed by this task.

## License

MIT; see [LICENSE](LICENSE). Review source-specific terms before redistribution or production use.
