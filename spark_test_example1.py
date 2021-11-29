from pyspark.sql import SparkSession
from pyspark import StorageLevel

import sharp
import time

spark = SparkSession\
        .builder\
        .appName("Test1")\
        .getOrCreate()

N = 100000
ds1 = spark.range(0,N,2)
ds2 = spark.range(0,N,3)
ds3 = spark.range(0,N,4)

merged = ds1.join(ds2,"id").join(ds3,"id")
# merged.persist(StorageLevel.MEMORY_ONLY)

ds4 = merged.filter(merged['id'] % 5 == 0)
ds5 = merged.filter(merged['id'] % 6 == 0)
ds6 = merged.filter(merged['id'] % 7 == 0)

final = ds4.join(ds5,"id").join(ds6,"id")
val = final.groupBy().sum()

start = time.time()
sharp.optimize(val)
end = time.time()
print("elapsed time : ",end - start)
