package spark

import org.apache.spark.sql.SparkSession
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.{HashingTF, IDF, RegexTokenizer, StopWordsRemover, Normalizer}
import org.apache.spark.sql.functions._
import org.apache.spark.ml.linalg.{Vector, Vectors}
import java.io.{File, PrintWriter}
// import com.harito.spark.Utils._

object Lab17_NLPPipeline {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder
      .appName("NLP Pipeline Example")
      .master("local[*]")
      .getOrCreate()

    import spark.implicits._
    println("Spark Session created successfully.")
    println(s"Spark UI available at http://localhost:4040")
    println("Pausing for 10 seconds to allow you to open the Spark UI...")
    Thread.sleep(10000)

    // 1. --- Read Dataset ---
    val readStartTime = System.nanoTime()
    val dataPath = "D:/NLP/data/c4-train.00000-of-01024-30K.json.gz"
    val initialDF = spark.read.json(dataPath).limit(args(0).toInt) // Limit for faster processing during lab
    val readDuration = (System.nanoTime() - readStartTime) / 1e9d
    println(f"--> Reading ${initialDF.count()} records took $readDuration%.2f seconds.")
    initialDF.printSchema()
    println("\nSample of initial DataFrame:")
    initialDF.show(5, truncate = false)

    // --- Pipeline Stages Definition ---

    // 2. --- Tokenization ---
    val tokenizer = new RegexTokenizer()
      .setInputCol("text")
      .setOutputCol("tokens")
      .setPattern("\\s+|[.,;!?()\"']") // Fix: Use \\s for regex, and \" for double quote

    /*
    // Alternative Tokenizer: A simpler, whitespace-based tokenizer.
    val tokenizer = new Tokenizer().setInputCol("text").setOutputCol("tokens")
    */

    // 3. --- Stop Words Removal ---
    val stopWordsRemover = new StopWordsRemover()
      .setInputCol(tokenizer.getOutputCol)
      .setOutputCol("filtered_tokens")

    // 4. --- Vectorization (Term Frequency) ---
    // Convert tokens to feature vectors using HashingTF (a fast way to do count vectorization).
    // setNumFeatures defines the size of the feature vector. This is the maximum number of features
    // (dimensions) in the output vector. Each word is hashed to an index within this range.
    //
    // If setNumFeatures is smaller than the actual vocabulary size (number of unique words),
    // hash collisions will occur. This means different words will map to the same feature index.
    // While this leads to some loss of information, it allows for a fixed, manageable vector size
    // regardless of how large the vocabulary grows, saving memory and computation for very large datasets.
    // 20,000 is a common starting point for many NLP tasks.
    val hashingTF = new HashingTF()
      .setInputCol(stopWordsRemover.getOutputCol)
      .setOutputCol("raw_features")
      .setNumFeatures(20000) // Set the size of the feature vector

    // 5. --- Vectorization (Inverse Document Frequency) ---
    val idf = new IDF()
      .setInputCol(hashingTF.getOutputCol)
      .setOutputCol("features")

    // // 6. --- Assemble the Pipeline ---
    // val pipeline = new Pipeline()
    //   .setStages(Array(tokenizer, stopWordsRemover, hashingTF, idf))
    
    // 6. --- Normalization ---
    val normalizer = new Normalizer()
      .setInputCol(idf.getOutputCol)
      .setOutputCol("normalized_features")
      .setP(2.0) // L2 normalization (Euclidean norm)

    // 7. --- Assemble the Pipeline ---
    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, stopWordsRemover, hashingTF, idf, normalizer))

    // --- Time the main operations ---

    println("\nFitting the NLP pipeline...") // Fix: Ensure single-line string literal
    val fitStartTime = System.nanoTime()
    val pipelineModel = pipeline.fit(initialDF)
    val fitDuration = (System.nanoTime() - fitStartTime) / 1e9d
    println(f"--> Pipeline fitting took $fitDuration%.2f seconds.")

    println("\nTransforming data with the fitted pipeline...") // Fix: Ensure single-line string literal
    val transformStartTime = System.nanoTime()
    val transformedDF = pipelineModel.transform(initialDF)
    transformedDF.cache() // Cache the result for efficiency
    val transformCount = transformedDF.count() // Force an action to trigger the transformation
    val transformDuration = (System.nanoTime() - transformStartTime) / 1e9d
    println(f"--> Data transformation of $transformCount records took $transformDuration%.2f seconds.")

    // Calculate actual vocabulary size after tokenization and stop word removal
    val vocabStartTime = System.nanoTime()
    val actualVocabSize = transformedDF
      .select(explode($"filtered_tokens").as("word"))
      .filter(length($"word") > 1)
      .distinct()
      .count()
    val vocabDuration = (System.nanoTime() - vocabStartTime) / 1e9d
    println(f"--> Calculating vocabulary size took $vocabDuration%.2f seconds.")
    println(s"--> Actual vocabulary size after tokenization and stop word removal: $actualVocabSize unique terms.")

    // --- Show and Save Results ---
    println("\nSample of transformed data:") // Fix: Ensure single-line string literal
    transformedDF.select("text", "normalized_features").show(5, truncate = 50)

    val n_results = 20
    val results = transformedDF.select("text", "features", "normalized_features").take(n_results)

    // 7. --- Write Metrics and Results to Separate Files ---

    // Write metrics to the log folder
    val log_path = "../log/lab17_metrics.log" // Corrected path
    new File(log_path).getParentFile.mkdirs() // Ensure directory exists
    val logWriter = new PrintWriter(new File(log_path))
    try {
      logWriter.println("--- Performance Metrics ---")
      logWriter.println(f"Data reading duration: $readDuration%.2f seconds")
      logWriter.println(f"Pipeline fitting duration: $fitDuration%.2f seconds")
      logWriter.println(f"Data transformation duration: $transformDuration%.2f seconds")
      logWriter.println(f"Vocabulary size calculation duration: $vocabDuration%.2f seconds")
      logWriter.println(s"Actual vocabulary size (after preprocessing): $actualVocabSize unique terms")
      logWriter.println(s"HashingTF numFeatures set to: 20000")
      if (20000 < actualVocabSize) {
        logWriter.println(s"Note: numFeatures (20000) is smaller than actual vocabulary size ($actualVocabSize). Hash collisions are expected.")
      }
      logWriter.println(s"Metrics file generated at: ${new File(log_path).getAbsolutePath}")
      logWriter.println("\nFor detailed stage-level metrics, view the Spark UI at http://localhost:4040 during execution.")
      println(s"\nSuccessfully wrote metrics to $log_path")
    } finally {
      logWriter.close()
    }

    // Write data results to the results folder
    val result_path = "../results/lab17_pipeline_output.txt" // Corrected path
    new File(result_path).getParentFile.mkdirs() // Ensure directory exists
    val resultWriter = new PrintWriter(new File(result_path))
    try {
      resultWriter.println(s"--- NLP Pipeline Output (First $n_results results) ---")
      resultWriter.println(s"Output file generated at: ${new File(result_path).getAbsolutePath}\n")
      results.foreach { row =>
        val text = row.getAs[String]("text")
        val features = row.getAs[org.apache.spark.ml.linalg.Vector]("features")
        val n_features = row.getAs[Vector]("normalized_features")
        resultWriter.println("="*80)
        resultWriter.println(s"Original Text: ${text.substring(0, Math.min(text.length, 100))}...")
        resultWriter.println(s"TF-IDF Vector: ${features.toString}")
        resultWriter.println(s"Normalized TF-IDF Vector: ${n_features.toString}")
        resultWriter.println("="*80)
        resultWriter.println()
      }
      println(s"Successfully wrote $n_results results to $result_path")
    } finally {
      resultWriter.close()
    }

    // --- Find Similar Documents ---
    println("\nFinding similar documents...")
    val similarityStartTime = System.nanoTime()

    // Select a random document (first document for simplicity) and ensure it has valid features
    val referenceDocOption = transformedDF
      .select("text", "normalized_features")
      .filter($"normalized_features".isNotNull)
      .first()

    if (referenceDocOption == null) {
      println("Error: No valid reference document found with non-null features.")
    } else {
      val referenceText = referenceDocOption.getAs[String]("text")
      val referenceVector = referenceDocOption.getAs[Vector]("normalized_features")

      // Create a single-row DataFrame for the reference vector
      val referenceDF = Seq((referenceText, referenceVector)).toDF("ref_text", "ref_features")

      // Define cosine similarity UDF
      val cosineSimilarityUDF = udf { (v1: Vector, v2: Vector) =>
        if (v1 == null || v2 == null) {
          0.0 // Return 0 similarity for null vectors
        } else {
          val dotProduct = v1.toArray.zip(v2.toArray).map { case (x, y) => x * y }.sum
          dotProduct // Since vectors are L2-normalized, dot product equals cosine similarity
        }
      }

      // Cross join to compare reference vector with all documents
      val similarities = transformedDF
        .crossJoin(referenceDF)
        .withColumn("similarity", cosineSimilarityUDF($"normalized_features", $"ref_features"))
        .select($"text", $"similarity")
        .filter($"similarity".isNotNull && $"text" =!= referenceText) // Exclude reference document
        .orderBy($"similarity".desc)
        .limit(5) // Get top 5 similar documents

      // Show top 5 similar documents
      println("\nReference Document:")
      println(s"Text: ${referenceText.substring(0, Math.min(referenceText.length, 100))}...")
      println("\nTop 5 Similar Documents:")
      similarities.show(5, truncate = 50)

      // Write similarity results to file
      val similarityResultPath = "../results/lab17_similarity_output.txt"
      new File(similarityResultPath).getParentFile.mkdirs()
      val similarityWriter = new PrintWriter(new File(similarityResultPath))
      try {
        similarityWriter.println("--- Top 5 Similar Documents ---")
        similarityWriter.println(s"Reference Document: ${referenceText.substring(0, Math.min(referenceText.length, 100))}...")
        similarityWriter.println("\nTop 5 Similar Documents:")
        similarities.collect().foreach { row =>
          val text = row.getAs[String]("text")
          val similarity = row.getAs[Double]("similarity")
          similarityWriter.println("="*80)
          similarityWriter.println(s"Text: ${text.substring(0, Math.min(text.length, 100))}...")
          similarityWriter.println(f"Cosine Similarity: $similarity%.4f")
          similarityWriter.println("="*80)
          similarityWriter.println()
        }
        similarityWriter.println(s"Output file generated at: ${new File(similarityResultPath).getAbsolutePath}")
        println(s"Successfully wrote similarity results to $similarityResultPath")
      } finally {
        similarityWriter.close()
      }
    }

    val similarityDuration = (System.nanoTime() - similarityStartTime) / 1e9d
    println(f"--> Finding similar documents took $similarityDuration%.2f seconds.")

    spark.stop()
    println("Spark Session stopped.")
  }
}
