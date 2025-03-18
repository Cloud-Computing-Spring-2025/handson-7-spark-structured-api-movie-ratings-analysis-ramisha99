from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, lit
def initialize_spark(app_name="Task2_Churn_Risk_Users"):
    """
    Initialize and return a SparkSession.
    """
    spark = SparkSession.builder \
        .appName(app_name) \
        .getOrCreate()
    return spark

def load_data(spark, file_path):
    """
    Load the movie ratings data from a CSV file into a Spark DataFrame.
    """
    schema = """
        UserID INT, MovieID INT, MovieTitle STRING, Genre STRING, Rating FLOAT, ReviewCount INT, 
        WatchedYear INT, UserLocation STRING, AgeGroup STRING, StreamingPlatform STRING, 
        WatchTime INT, IsBingeWatched BOOLEAN, SubscriptionStatus STRING
    """
    df = spark.read.csv(file_path, header=True, schema=schema)
    return df

def identify_churn_risk_users(df):
    """
    Identify users with canceled subscriptions and low watch time (<100 minutes).

    Steps:
    1. Filter users where `SubscriptionStatus = 'Canceled'` AND `WatchTime < 100`.
    2. Count the number of such users.
    3. Format the output to include a descriptive row.
    """

    # Step 1: Filter churn-risk users
    churn_risk_df = df.filter((col("SubscriptionStatus") == "Canceled") & (col("WatchTime") < 100))

    # Step 2: Count churn-risk users
    churn_risk_count = churn_risk_df.agg(count("UserID").alias("TotalUsers"))

    # Step 3: Add a descriptive column
    result_df = churn_risk_count.withColumn("Churn Risk Users", lit("Users with low watch time & canceled subscriptions"))

    # Step 4: Reorder columns to match expected output
    result_df = result_df.select("Churn Risk Users", "TotalUsers")

    return result_df


def write_output(result_df, output_path):
    """
    Write the result DataFrame to a CSV file.
    """
    result_df.coalesce(1).write.csv(output_path, header=True, mode='overwrite')

def main():
    """
    Main function to execute Task 2.
    """
    spark = initialize_spark()

    input_file = "/workspaces/handson-7-spark-structured-api-movie-ratings-analysis-ramisha99/input/movie_ratings_data.csv"
    output_file = "/workspaces/handson-7-spark-structured-api-movie-ratings-analysis-ramisha99/outputs/churn_risk_users.csv"

    df = load_data(spark, input_file)
    result_df = identify_churn_risk_users(df)
    write_output(result_df, output_file)

    spark.stop()

if __name__ == "__main__":
    main()
