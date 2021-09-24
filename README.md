# spark-on-k8-with-adls-connectivity
This repo contains configurations and dockerfile to generate a image, which can be deployed on self-managed kubernetes cluster to run spark jobs. Key configuration is it has the configurations such that it can access data from adls gen 2 (directly via abfs: link))

key points:
Use Spark-installation which comes without hadoop: spark-without-hadoop
  for spark-without-hadoop; if you try to run spark-submit without setting SPARK_DIST_CLASSPATH=$(hadoop classpath), we wont be able to run spark-submit, as it will not have hadoop jars inbuilt
  Add azure and datalake jars to SPARK_DIST_CLASSPATH as well to make spark able to access abfs: if we want hadoop to hdfs dfs to access adls too, then add this azure and datalake jars present in hadoop/share/hadoop/tools/lib to HADOOP_CLASSPATH as well.
  
We need to add a new property in hadoop core-site.xml realted to our azure account credentails as shown in core-site.xml file in repo.


Use ENV in dockerfile rather then using RUN export..., as export will not persist till the final docker image and will vanish from intermedate steps, while ENV will.

We wont be able to run this image as an individual container as it expects itlsef to be submitted with spark-submit or with SparkApplication only.



Some steps to make spark and hadoop up and running:

- get a image with proper jdk installed ; we are using openjdk:8-jre-slim
- get hadoop and spark-wiithout-hadoop using wget on image
- extract
- First, setup hadoop:
	extract	
	edit hadoop-env.sh and add "export JAVA_HOME=<patj to jdk>"
	export HADOOP_HOME to env
	add HADOOP_HOME/bin and HADOOP_HOME/sbin to PATH
	now "hadoop classpath" command should work on terminal
- Second, setup spark-without-hadoop:
	extract
	export SPARK_HOME to env
	add SPARK_HOME/bin and SPARK_HOME/sbin to PATH
	export SPARK_DIST_CLASSPATH=<output of hadoop classpath>
	now "spark-submit" should run on terminal

  
  
