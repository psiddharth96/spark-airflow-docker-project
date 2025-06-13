## Project Overview
This project is intended to cover basic spark standalone cluster setup workflow in docker containerized setup.
Anyone with this setup can be able to do simple pocs with most commonly required features of spark, airflow such as Spark Dags, History server, Airflow Dags setup
You can also add different kinds of data sinks or source such as postgresql database or many more like this.
One such Data Sink implemented in project is Postgresql

![image](https://github.com/user-attachments/assets/695bd0a1-5eca-44f5-963d-a8f2022e325f)


## Steps to start with setup and do simple pocs
1. Start docker engine
2. Run docker-compose up --scale spark-worker=3

   * This will create spark airflow environment with specified spark workers in a standalone cluster setup

4. Next step is to login to postgresql db at port 8888

   * Enter password and username given in env files

5. Check if spark master container and airflow containers are running at ports 9090 and 8099 respectively

   * If these ports are blocked then set ports accordingly in docker compose

6. Check if spark history server is running at port 18080

7. Setup spark connection with name spark [see details below] in airflow connections (airflow user name password is admin)

8. Airflow spark connection details - host is spark://spark-master & port will be 7077

9. Try running test dag under visible Dags in Airflow.

10. After done with development - docker-compose down


## Some considerations going forward
1. This is spark standalone cluster setup - In this cluster mode spark only allows spark submit in client mode
2. As spark only allows spark submit in client mode - it needs to be installed on airflow container as well, hence image size is large
