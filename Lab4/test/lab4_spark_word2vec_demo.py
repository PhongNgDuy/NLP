import os
import re
from pyspark.sql import SparkSession
from pyspark.ml.feature import Word2Vec
from pyspark.sql.functions import col, lower, regexp_replace, split, size

def main():
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    output_path = os.path.join(results_dir, "lab4_spark_output.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        def log(msg=""):
            print(msg)
            f.write(msg + "\n")

        log("=" * 60)
        log("Lab 4 - Spark Word2Vec Demonstration")
        log("=" * 60)

        data_path = r"D:\NLP\data\c4-train.00000-of-01024-30K.json.gz"
        log(f"Loading dataset from: {data_path}")

        # Initialize Spark Session
        spark = SparkSession.builder \
            .appName("SparkWord2VecLab4") \
            .master("local[*]") \
            .getOrCreate()

        # Load dataset
        df = spark.read.json(data_path)
        df = df.select("text").na.drop()

        # Text preprocessing
        df_clean = df.select(
            lower(col("text")).alias("text")
        ).select(
            regexp_replace(col("text"), r"[^a-z\s]", "").alias("text")
        ).select(
            split(col("text"), r"\s+").alias("words")
        )

        # Filter out empty/short documents
        df_clean = df_clean.filter(size(col("words")) >= 3)

        # Count statistics
        num_docs = df_clean.count()
        total_tokens = df_clean.rdd.map(lambda r: len(r["words"])).sum()
        avg_len = total_tokens / num_docs if num_docs > 0 else 0

        log(f"Documents loaded: {num_docs:,}")
        log(f"Total sentences: {num_docs:,}")
        log(f"Total tokens: {int(total_tokens):,}")
        log(f"Average tokens per document: {avg_len:.2f}")

        log("Training Spark Word2Vec model...")

        # Train Word2Vec model
        word2Vec = Word2Vec(
            vectorSize=100,
            minCount=5,
            inputCol="words",
            outputCol="result"
        )
        model = word2Vec.fit(df_clean)
        log("Training completed successfully.")

        # Vocabulary size
        vocab_size = len(model.getVectors().collect())
        log(f"Vocabulary size: {vocab_size:,}")

        log("=" * 60)
        log("Top 5 synonyms for 'computer':")
        synonyms = model.findSynonyms("computer", 5)
        for word, cosine_sim in synonyms.collect():
            log(f"  {word:15s}  {cosine_sim:.4f}")

        log("=" * 60)
        log("Spark Word2Vec demonstration completed.")
        log("Stopping Spark session...")
        spark.stop()
        log("Spark session stopped successfully.")
        log(f"Output saved to: {output_path}")

    print(f"\nLog saved successfully to: {output_path}")

if __name__ == "__main__":
    main()

