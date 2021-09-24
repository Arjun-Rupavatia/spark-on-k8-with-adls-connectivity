from pyspark.sql import SparkSession
from pyspark import SparkContext
#sc = SparkContext("local", "First App")
#sc.hadoopConfiguration.set("fs.azure.account.key.cieanalyticsstoragedev.dfs.core.windows.net", "fI59Mavwgl5+sms7p25JI7F1AeO1ZNifUiBee6g/ek0LVwqCUYqcdnMlw01IEQOO2UIHWVQWIsTflbfP0h8exw==")
#sc._jsc.hadoopConfiguration().set("fs.azure.account.key.cieanalyticsstoragedev.dfs.core.windows.net","fI59Mavwgl5+sms7p25JI7F1AeO1ZNifUiBee6g/ek0LVwqCUYqcdnMlw01IEQOO2UIHWVQWIsTflbfP0h8exw==")
spark = SparkSession.builder.getOrCreate()
df = spark.read.text("abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIETest/Aman/kafkatest1/azure_cost_tracking_2/record85.txt")
#df = spark.read.text("hdfs:///CIETest/Aman/kafkatest1/azure_cost_tracking_2/record85.txt")
#df.show()
#df = spark.read.text("hdfs://localhost:9000/record85.txt")   this is working
df.show()

print("I -------------------- AM -----------Working!!!!!!!!!")
