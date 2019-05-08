import org.apache.kafka.common.serialization.StringDeserializer
import org.apache.spark._
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.streaming._
import org.apache.spark.streaming.kafka010.LocationStrategies.PreferConsistent
import org.apache.spark.streaming.kafka010._

object slackConsumer {

  def main(args: Array[String]): Unit = {

    // Spark Config
    val conf = new SparkConf()
      .setAppName("kafka-spark-streaming")
      .setMaster("local[*]")

    val ssc = new StreamingContext(conf, Seconds(7))

    // Kafka Config
    val topics = List("slackMessages").toSet
    val test_kafka = "localhost:9092"
    val sandbox_kafka = "sandbox.hortonworks.com:6667"
    val outpath= "hdfs://sandbox.hortonworks.com:8020/user/maria_dev/slackbot_out"

    //Change map of bootstrap servers to sandbox_kafka when using for hortonworks
    val kafkaParams = Map(
      "bootstrap.servers" -> sandbox_kafka,
      "key.deserializer" -> classOf[StringDeserializer],
      "value.deserializer" -> classOf[StringDeserializer],
      "group.id" -> "slack", // Your consumer group
      "auto.offset.reset" -> "earliest")

    // Getting the Data from Kafka into Dstream Object
    val kafka_stream_Dstream = KafkaUtils.createDirectStream[String,String](
      ssc,
      PreferConsistent,
      ConsumerStrategies.Subscribe[String, String](topics, kafkaParams))

    val lower_Dstream = kafka_stream_Dstream.map(record => record.value().toString)

    lower_Dstream.foreachRDD { rddRaw =>

      if (!rddRaw.isEmpty) {

        val spark = SparkSession.builder.config(rddRaw.sparkContext.getConf).enableHiveSupport().getOrCreate()

        val df = spark.read.json(rddRaw)

        val resultDF = df.select(
          col("screen_name"),
          col("user").alias("user_id"),
          col("channel"),
          col("event_ts").cast("double").cast("timestamp").alias("time"),
          col("text")
          )

        resultDF.show(5)
        resultDF.printSchema()

        resultDF
          .withColumn("date", date_format(col("time"), "YYYYMMdd"))
          .withColumn("hour", hour(col("time")))
          .write
          .mode("append")
          .partitionBy("date", "hour")
          .format("orc")
          .save(outpath)

      }
    }

    ssc.start()
    ssc.awaitTermination()
  }

}
