import os
import pandas as pd
import dask.dataframe as dd
from tqdm import tqdm
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


class DBConn:
    """Class to manage the Edge IIoT SQLite database."""

    def __init__(self, db_name: str, db_dir: str):
        self.db_path = os.path.join(db_dir, db_name)
        os.makedirs(db_dir, exist_ok=True)

    def create_database(self, csv_files: list) -> None:
        """
        Creates a SQLite database from a list of CSV files.
        """

        print(f"Uploading CSV files to {self.db_path}")
        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                for csv_file in tqdm(csv_files, unit="file", ncols=50):
                    chunks = pd.read_csv(csv_file, chunksize=5000, low_memory=False)
                    table_name = os.path.splitext(os.path.basename(csv_file))[0]
                    for chunk in chunks:
                        chunk.to_sql(table_name, conn, if_exists="append", index=False)
        except SQLAlchemyError as e:
            print(f"Error creating database: {e}")

    def table_names(self) -> list:
        """
        Return the names of all tables in the database.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                tables = conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table';")
                ).fetchall()
            return [table[0] for table in tables]
        except SQLAlchemyError as e:
            print(f"Error getting table names: {e}")

    def get_shape(self, table_name: str) -> tuple:
        """
        Return the shape (row count, column count) of a specific table in the database.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                rows = conn.execute(
                    text(f"SELECT COUNT(*) FROM {table_name};")
                ).fetchone()[0]
                cols = conn.execute(
                    text(f"PRAGMA table_info({table_name});")
                ).fetchall()
            return format(rows, "_d"), len(cols)
        except SQLAlchemyError as e:
            print(f"Error getting shape: {e}")

    def get_table(self, table_name: str, chunk_size: int = 4000) -> dd.DataFrame:
        """
        Return a Dask DataFrame of a specific table in the database, loaded in chunks using Pandas.
        """
        
        db_uri = f"sqlite:///{self.db_path}"
        query = f"SELECT * FROM {table_name};"
        dask_chunks = []  # Store each chunk as a Dask DataFrame

        try:
            # Use Pandas to read data in chunks
            for chunk in pd.read_sql_query(query, db_uri, chunksize=chunk_size):
                # Process each chunk as needed
                processed_chunk = self.process_chunk(chunk)

                # Convert Pandas chunk to Dask DataFrame and append to list
                dask_chunk = dd.from_pandas(processed_chunk, npartitions=1)
                dask_chunks.append(dask_chunk)

            # Concatenate all Dask chunks into a single Dask DataFrame
            full_ddf = dd.concat(dask_chunks, axis=0)
            return full_ddf

        except Exception as e:
            print(f"Error getting table: {e}")

    def process_chunk(self, chunk: pd.DataFrame) -> pd.DataFrame:
        """
        Optional processing method for each chunk, to filter, transform, etc.
        """
        
        # chunk = chunk.dropna()
        # chunk = chunk.drop_duplicates()

        return chunk

    def get_rows(self, table_name: str, n_rows: int) -> pd.DataFrame:
        """
        Return a DataFrame of the first n_rows of a specific table in the database.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                table = pd.read_sql_query(
                    text(f"SELECT * FROM {table_name} LIMIT {n_rows};"), conn
                )
            return table
        except SQLAlchemyError as e:
            print(f"Error getting rows: {e}")

    def get_columns(self, table_name: str) -> list:
        """
        Return a list of column names in a specific table in the database.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                cols = conn.execute(
                    text(f"PRAGMA table_info({table_name});")
                ).fetchall()
            return [col[1] for col in cols]
        except SQLAlchemyError as e:
            print(f"Error getting columns: {e}")

    def merge_tables(self, table_names: list, new_table_name: str) -> None:
        """
        Merge multiple tables into a new table using UNION ALL.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{new_table_name}';"
                table_exists = conn.execute(text(table_exists_query)).fetchone()
                if table_exists:
                    print(
                        f"Table '{new_table_name}' already exists. Merge operation aborted."
                    )
                    return
                union_query = " UNION ALL ".join(
                    [f"SELECT * FROM {table}" for table in table_names]
                )
                create_table_query = f"CREATE TABLE {new_table_name} AS {union_query};"
                conn.execute(text(create_table_query))
                print(f"Merged tables {table_names} into {new_table_name}")
        except SQLAlchemyError as e:
            print(f"Error merging tables: {e}")

    def drop_table(self, table_name: str) -> None:
        """
        Drop a table from the database.
        """

        engine = create_engine(f"sqlite:///{self.db_path}")
        try:
            with engine.connect() as conn:
                conn.execute(text(f"DROP TABLE {table_name};"))
            print(f"Dropped table {table_name}")
        except SQLAlchemyError as e:
            print(f"Error dropping table: {e}")
