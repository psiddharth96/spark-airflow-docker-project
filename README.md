Project Overview
This project is intended to cover basic spark standalone cluster setup workflow in docker containerized setup.
Anyone with this setup can be able to do simple pocs with most commonly required features of spark, airflow such as Spark Dags, History server, Airflow Dags setup
You can also add different kinds of data sinks or source such as postgresql database or many more like this.
One such Data Sink implemented in project is Postgresql
Steps to start with setup and do simple pocs
start docker engine

Run docker-compose up --scale spark-worker=3

This will create spark airflow environment with specified spark workers in a standalone cluster setup
Next step is to login to postgresql db at port 8888

Enter password and username given in env files

Check if spark master container and airflow containers are running at ports 9090 and 8099 respectively

If these ports are blocked then set ports accordingly in docker compose
Check if spark history server is running at port 18080

Setup spark connection with name spark [see details below] in airflow connections (airflow user name password is admin)

Airflow spark connection details - host is spark://spark-master & port will be 7077

Try running test dag under visible Dags in Airflow.

After done with development - docker-compose down

New File at / · psiddharth96/spark-airflow-docker-project
