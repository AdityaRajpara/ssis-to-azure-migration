# Benchmarking

Run `python -m migration_demo.cli benchmark --iterations 5` after installing the project. The command executes each pipeline implementation against the same bundled snapshot in isolated temporary directories, then reports per-run wall-clock seconds, median seconds, and canonical Gold output bytes in `artifacts/benchmark.json`.

The bundled input is intentionally tiny, so local timings mostly measure interpreter and filesystem overhead. Compare larger, representative snapshots on the same host/runtime and repeat runs before drawing conclusions. These measurements are not Azure cost estimates and must not be translated into cost-saving percentages. For cloud cost comparison, collect Azure Cost Management and workload telemetry over comparable windows and normalize for volume/SLA.
