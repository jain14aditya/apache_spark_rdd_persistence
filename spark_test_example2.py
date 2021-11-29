from pyspark.sql import SparkSession
import time

spark = SparkSession\
        .builder\
        .appName("Test2")\
        .getOrCreate()

N = 10000
df1 = spark.range(0,N,2)
df2 = df1.withColumn('id',df1.id ** 2)
df3 = df2.filter(df2['id'] <= 1000)
df4 = df2.filter(df2['id'] >= 9000)
df5 = df3.union(df4)
sum = df5.selectExpr("sum(id)")

start = time.time()
print(sum.show())
end = time.time()
print("elapsed time : ",end - start)

# print(sum.explain(mode="formatted"))