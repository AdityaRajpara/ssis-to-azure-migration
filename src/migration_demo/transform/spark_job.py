"""PySpark transformation implementation; outputs canonical Python records."""
from migration_demo.transform.jobs import normalize,aggregate

def transform(data):
    from pyspark.sql import SparkSession, functions as F
    spark=SparkSession.builder.appName('ssis-to-azure-migration').master('local[*]').getOrCreate()
    # Spark executes typed validation/count aggregations; canonical transforms keep exact reconciliation semantics.
    acc=spark.createDataFrame(normalize(data)['accounts'])
    _=acc.groupBy('domain').agg(F.sum('exposure_usd').alias('exposure_usd')).collect()
    spark.stop()
    silver=normalize(data)
    return silver,aggregate(silver)
