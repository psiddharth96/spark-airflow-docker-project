from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark import SparkConf


if __name__ == "__main__":
    conf = SparkConf()
    conf.set("spark.app.name", "DemoApp")
    
    spark = SparkSession.builder \
            .config(conf=conf) \
            .getOrCreate()
            
    demoData = [('Afple', 25),('Banane', 24)]
    df = spark.createDataFrame(demoData).toDF("Obst", "Preis")
    
    
    
    df.show()
    input("Press Enter...")