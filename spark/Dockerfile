FROM ubuntu:22.04 AS spark-base

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      sudo \
      curl \
      vim \
      nano \
      unzip \
      rsync \
      openjdk-11-jdk \
      python3 \
      python3-pip \
      software-properties-common \
      ssh && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Define default values directly
ENV SPARK_HOME="/opt/spark"
ENV HADOOP_HOME="/opt/hadoop"


RUN mkdir -p ${HADOOP_HOME} && mkdir -p ${SPARK_HOME}
WORKDIR ${SPARK_HOME}

RUN curl -L https://archive.apache.org/dist/spark/spark-3.3.1/spark-3.3.1-bin-hadoop3.tgz -o spark.tgz \
    && mkdir -p /opt/spark \
    && tar -xvzf spark.tgz --strip-components=1 -C /opt/spark \
    && rm spark.tgz

FROM spark-base AS pyspark

# Install python deps
COPY requirements/requirements.txt .
RUN pip3 install -r requirements.txt

ENV PATH="/opt/spark/sbin:/opt/spark/bin:${PATH}"
ENV SPARK_HOME="/opt/spark"
ENV SPARK_MASTER="spark://spark-master:7077"
ENV SPARK_MASTER_HOST=spark-master
ENV SPARK_MASTER_PORT=7077
ENV PYSPARK_PYTHON=python3

COPY conf/spark-defaults.conf "$SPARK_HOME/conf"

RUN chmod u+x /opt/spark/sbin/* && \
    chmod u+x /opt/spark/bin/*

ENV PYTHONPATH=$SPARK_HOME/python/
ENV PYTHONPATH=$PYTHONPATH:/opt/spark/python/lib/

# Add link between python3 and python so that you can use python main.py in terminal instead of python3
RUN ln -s /usr/bin/python3 /usr/bin/python

COPY entrypoint.sh .

ENTRYPOINT ["./entrypoint.sh"]