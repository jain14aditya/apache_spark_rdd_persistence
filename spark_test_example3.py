from pyspark.sql import SparkSession
from pyspark.sql.functions import when
from pyspark.sql.functions import udf
from pyspark.sql.types import BooleanType
import pyspark.sql.functions as f
from pyspark import StorageLevel

import sharp

import time

spark = SparkSession\
        .builder\
        .appName("Test3")\
        .getOrCreate()

N = 1000000
df1 = spark.range(2,N)

df2 = df1.filter((f.col('id') == 2) | (f.col('id') % 2 != 0))

df3 = df2.filter((f.col('id') == 3) | (f.col('id') % 3 != 0))

df5 = df3.filter((f.col('id') == 5) | (f.col('id') % 5 != 0))
# df5.persist(StorageLevel.MEMORY_ONLY)

df7 = df5.filter((f.col('id') == 7) | (f.col('id') % 7 != 0))
df11 = df5.filter((f.col('id') == 11) | (f.col('id') % 11 != 0))
df13 = df5.filter((f.col('id') == 13) | (f.col('id') % 13 != 0))
df17 = df5.filter((f.col('id') == 17) | (f.col('id') % 17 != 0))
df19 = df5.filter((f.col('id') == 19) | (f.col('id') % 19 != 0))

df23 = df7.filter((f.col('id') == 23) | (f.col('id') % 23 != 0))
df29 = df7.filter((f.col('id') == 29) | (f.col('id') % 29 != 0))

df31 = df11.filter((f.col('id') == 31) | (f.col('id') % 31 != 0))
df37 = df11.filter((f.col('id') == 37) | (f.col('id') % 37 != 0))

df41 = df13.filter((f.col('id') == 41) | (f.col('id') % 41 != 0))
df43 = df13.filter((f.col('id') == 43) | (f.col('id') % 43 != 0))

df53 = df17.filter((f.col('id') == 53) | (f.col('id') % 53 != 0))
df59 = df17.filter((f.col('id') == 59) | (f.col('id') % 59 != 0))

df61 = df19.filter((f.col('id') == 61) | (f.col('id') % 61 != 0))
df67 = df19.filter((f.col('id') == 67) | (f.col('id') % 67 != 0))

final = df23.join(df29,'id').join(df31,'id').join(df37,'id').join(df41,'id').join(df43,'id').join(df53,'id').join(df59,'id').join(df61,'id').join(df67,'id')

start = time.time()
print(final.show())
end = time.time()
print("elapsed time : ",end - start)

# print(final.explain(mode="formatted"))
sharp.optimize(final)