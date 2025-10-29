import os
import re
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col, lower, regexp_replace, split, size
from pyspark.sql.functions import when

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(project_root, "results")
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "lab5_sentiment_output.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        def log(msg=""):
            print(msg)
            f.write(msg + "\n")

        log("=" * 60)
        log("Lab 5 - Spark Sentiment Classification")
        log("=" * 60)

        # Khởi tạo Spark
        spark = SparkSession.builder \
            .appName("SparkSentimentClassification") \
            .master("local[*]") \
            .getOrCreate()

        # Đọc file CSV
        data_path = r"D:\NLP\data\sentiments.csv"  
        df = spark.read.csv(data_path, header=True, inferSchema=True)
        df = df.na.drop(subset=["text", "sentiment"])
        log(f"Loaded dataset from: {data_path}")
        log(f"Rows: {df.count()}, Columns: {len(df.columns)}")

        # Tiền xử lý text
        df_clean = df.select(
            lower(col("text")).alias("text"),
            col("sentiment").alias("label")
        ).select(
            regexp_replace(col("text"), r"[^a-z\s]", "").alias("text"),
            col("label")
        ).select(
            split(col("text"), r"\s+").alias("words"),
            col("label")
        )

        df_clean = df_clean.withColumn("label", when(col("label") == -1, 0).otherwise(col("label")))

        log(f"After cleaning: {df_clean.count()} samples remain.")

        # Word2Vec vectorization
        word2Vec = Word2Vec(
            vectorSize=100,
            minCount=1,
            inputCol="words",
            outputCol="features"
        )
        model = word2Vec.fit(df_clean)
        df_vec = model.transform(df_clean)

        log("Word2Vec embedding created.")

        # Tách train/test
        train_df, test_df = df_vec.randomSplit([0.8, 0.2], seed=42)

        # Huấn luyện Logistic Regression
        lr = LogisticRegression()
        lr_model = lr.fit(train_df)
        log("Training completed successfully.")

        # Dự đoán và đánh giá
        predictions = lr_model.transform(test_df)

        evaluator = MulticlassClassificationEvaluator(metricName="accuracy")
        accuracy = evaluator.evaluate(predictions)
        evaluator_f1 = MulticlassClassificationEvaluator(metricName="f1")
        f1 = evaluator_f1.evaluate(predictions)

        log(f"Accuracy: {accuracy:.4f}")
        log(f"F1-score: {f1:.4f}")

        log("=" * 60)
        log("Spark Sentiment Classification completed.")
        spark.stop()
        log("Spark session stopped successfully.")
        log(f"Output saved to: {output_path}")

    print(f"\nLog saved successfully to: {output_path}")

if __name__ == "__main__":
    main()
