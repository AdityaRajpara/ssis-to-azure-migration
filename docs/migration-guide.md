# Migration guide: SSIS package to cloud-native pipeline

## Legacy inventory (simulated)

`config/legacy_workflow.json` represents a scheduled package, connection managers, ordered control-flow tasks, retry policy, and failure behavior. The Python runner models extraction, staging, SQL-like transformations, validation, and publication. For a real migration, inventory SSISDB packages, environment variables, SQL Agent schedules, connection managers, file dependencies, script tasks, checkpoints, and operational SLAs before mapping components.

## Mapping

| SSIS pattern | Target example |
|---|---|
| Connection manager | ADF linked service with managed identity / Key Vault |
| Data Flow / source task | ADF Copy to ADLS Bronze |
| Execute SQL Task | PySpark transformation or Synapse SQL |
| Package precedence constraint | ADF activity dependency |
| SSISDB execution history | ADF Monitor, Azure Monitor alerts and Log Analytics |
| Package deployment | Git-backed ADF publish and CI/CD |
| SQL staging tables | ADLS Bronze and Silver |

## Cutover controls

1. Freeze and version source package/configuration; capture representative snapshots.
2. Build parallel cloud processing with idempotent run-date partitions and replay support.
3. Reconcile counts, keys, nulls, aggregates, and business totals per source and partition.
4. Review exceptions with owners; record tolerance and sign-off for rounding/time-zone differences.
5. Run shadow schedules, compare SLAs/cost telemetry, then cut over with rollback steps.
6. Retain lineage, owners, classifications, retention policy, and operational runbooks.

This repository only demonstrates repeatable local reconciliation on bundled samples. It does not simulate SSIS runtime semantics in full or claim a production cutover.
