from pyspark.sql.functions import *
from pyspark.sql import Window
from pyspark.sql import SparkSession
from pyspark import SparkContext

sc = SparkContext()
sc._jsc.hadoopConfiguration().set("fs.azure.account.key.cieanalyticsstoragedev.dfs.core.windows.net","fI59Mavwgl5+sms7p25JI7F1AeO1ZNifUiBee6g/ek0LVwqCUYqcdnMlw01IEQOO2UIHWVQWIsTflbfP0h8exw==")

def read_cost_distribution_data(basepath,date_list):
    path = []
    for date in date_list:
        path.append("{}/to_date={}/*".format(basepath,date))
    
    df = spark.read.parquet(*path)
    return df
    



def read_vp_mapping(filepath="abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIEConsumable/VPMapping/FinalVPMapping.csv"):
    
    mapp = spark.read.csv("abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIEConsumable/VPMapping/FinalVPMapping.csv",header=True)
    
#     mapp = spark.read.parquet(filepath)
#     mapp = mapp.withColumnRenamed("vpDisplayName","ExecutiveOwner")
#     mapp = mapp.withColumnRenamed("evpDisplayName","EvpName")
#     mapp = mapp.withColumnRenamed("projectUserDisplayName","productOwner")
    
    return mapp
    



    

def get_all_subfolder(basePath,topic):
    """Get all the subtopics in for a topic.
    We will do the processing on the subtopic
    level . 
    """
    import subprocess
    my_path = basePath + topic

    bashCommand = "hdfs dfs -ls {}".format(my_path)

    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    subtopics = [output.strip().split("\n")[i].split("/")[-1] for i in range(1,len(output.strip().split("\n")[:]))]
    
    return subtopics

def get_topic_dates(basePath, topic):
    
    from datetime import datetime as dt
    
    envs = get_all_subfolder(basePath,topic)
    dates = set()
    counter=0
    for env in envs:
        
        #print("-----------",env,"--------------")
        if counter == 0:
            dates = set(get_all_subfolder(basePath+topic+"/",env))
            counter+=1
        else:
            dates = dates & set(get_all_subfolder(basePath+topic+"/",env))
            
        
        
    dates = [i.split("=")[-1] for i in dates if i.startswith("to_date")==True]
    
    return dates

               

def get_dates(usageOutputPath, topic, subfolder):
    
    from datetime import datetime as dt
    
    envs = get_all_subfolder(usageOutputPath,topic)
    
    dates = set(get_all_subfolder(usageOutputPath+topic+"/",subfolder))
            
        
        
    dates = [i.split("=")[-1] for i in dates if i.startswith("to_date")==True]
    
    return dates

    
    
def get_dates_to_be_processed(baseOutputPath = "abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIEConsumable/",usage_topic = "K8UsageCostDistribution"):
    
    
    
    usage_dates = get_dates(baseOutputPath, usage_topic, "cost_distribution")
    
    output_dates = get_dates(baseOutputPath, usage_topic, "vp_cost_distribution")
            
    
    
    
    common_dates = set(usage_dates) - set(output_dates)
    
    
    return common_dates
    

def unionAll(*dfs):

    from functools import reduce  # For Python 3.x
    from pyspark.sql import DataFrame
    return reduce(lambda df1, df2: df1.union(df2.select(df1.columns)), dfs)
    #return reduce(DataFrame.unionAll, dfs)



    
def main(baseOutputPath,usage_topic):
    
    #date_list = get_dates_to_be_processed(baseOutputPath = "/CIEConsumable/",usage_topic = "K8UsageCostDistribution")
    date_list = ["20210910"]
    if len(date_list)==0:
        return
        

    df_usage = read_cost_distribution_data("abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIEConsumable/K8UsageCostDistribution/cost_distribution/",date_list)
    df_usage = df_usage.withColumnRenamed("dateTime","to_date")

    req_cols = ['namespace', 'environment', 'requested_cores', 'usage_cores', 
                'requested_core_proportion', 'requested_core_cost', 'usage_core_cost', 
                'wasted_cost', 'avg_req_cores_per_hour', 'avg_usage_cores_per_hour','to_date'
                ]

    df_usage = df_usage.select(*req_cols)
    df_usage = df_usage.toDF(*req_cols)

    vp_map = read_vp_mapping()
    ans = df_usage.join(vp_map,on = ["namespace","environment"],how="left")
    
    output_path = "{}{}/{}".format(baseOutputPath,usage_topic,"vp_cost_distribution")
    #ans.repartition(1).write.parquet(output_path, partitionBy = ["to_date"], mode = "append")
    print(ans.show())


if __name__=="__main__":
    
    spark = SparkSession.builder.getOrCreate()
    baseOutputPath = "abfs://spark-analytics-cie-dev-2020-10-26t21-36-45-237z@cieanalyticsstoragedev.dfs.core.windows.net/CIEConsumable/"
    usage_topic = "K8UsageCostDistribution"
    main(baseOutputPath,usage_topic)
