from pyspark.sql import SparkSession
from pyspark import SparkContext
#sc = SparkContext("local", "First App")
#sc.hadoopConfiguration.set("fs.azure.account.key.<account>.dfs.core.windows.net", "<key>")
#sc._jsc.hadoopConfiguration().set("fs.azure.account.key.<account>.dfs.core.windows.net","<key>")
spark = SparkSession.builder.getOrCreate()
df = spark.read.text("abfs://path/record85.txt")
#df = spark.read.text("hdfs://hdfs_path/record85.txt")
#df.show()
#df = spark.read.text("hdfs://localhost:9000/record85.txt")   this is working
df.show()

print("I -------------------- AM -----------Working!!!!!!!!!")
