import time
from src import dataset, database


# Some constants
url = "mohamedamineferrag/edgeiiotset-cyber-security-dataset-of-iot-iiot"
docs = ["edge_iiotset__datasetfl.pdf", "readme.txt"]
data = ["attack_traffic", "normal_traffic", "selected_dataset_for_ml_and_dl"]
docs_dir = "docs"
db_dir = "db"
temp_dir = "db/temp"
data_dir = "db/data"
db_name = "edge_iiotset.db"


def main() -> None:
    """
    Run ETL and deploy database.
    """

    start_time = time.time()
    file_ops = dataset.FileOps()
    iiotset_db = database.DBConn(db_name, db_dir)

    # Download and unzip dataset
    file_ops.fetch_dataset(url, temp_dir)
    time.sleep(20)
    file_ops.decompress_files(url, temp_dir)
    time.sleep(20)

    # Organize directories and files
    file_ops.normalize_paths(temp_dir)
    file_ops.move_items(data, temp_dir, data_dir)
    file_ops.move_items(docs, temp_dir, docs_dir)
    file_ops.delete_directory(temp_dir)

    # Build database and retrieve table information
    csv_files = file_ops.find_files(data_dir, ".csv")
    iiotset_db.create_database(csv_files)
    end_time = time.time()

    print(f"Elapsed time: {(end_time - start_time)/60:.2f} minutes")


if __name__ == "__main__":
    main()
