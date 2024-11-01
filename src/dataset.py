import os
import shutil
import zipfile
from tqdm import tqdm
from kaggle.api.kaggle_api_extended import KaggleApi


class FileOps:
    """Class to manage Edge IIoT dataset."""

    def __init__(self):
        self.api = KaggleApi()
        self.api.authenticate()

    def fetch_dataset(self, dataset: str, destination: str) -> None:
        """
        Download the dataset as a zip file to the destination directory.
        """

        self.api.dataset_download_files(dataset, path=destination, quiet=False)

    def decompress_files(self, dataset: str, destination: str) -> None:
        """
        Decompress the contents of the zip file to a destination directory.
        """

        zip_file_name = f"{dataset.split('/')[-1]}.zip"
        zip_file_path = os.path.join(destination, zip_file_name)

        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            total_size = sum((file.file_size for file in zip_ref.infolist()))
            print(f"Extracting datasets to {destination}")
            with tqdm(
                total=total_size, unit="B", unit_scale=True, ncols=50, leave=True
            ) as pbar:
                for file in zip_ref.infolist():
                    zip_ref.extract(file, destination)
                    pbar.update(file.file_size)
        print()

    def normalize_paths(self, root_dir: str, depth: int = 0) -> None:
        """
        Normalize the paths of directories and files by replacing spaces and hyphens with underscores.
        """

        for filename in os.listdir(root_dir):
            path = os.path.join(root_dir, filename)
            if os.path.isdir(path):
                self.normalize_paths(path, depth + 1)
                new_name = filename.lower().replace(" ", "_").replace("-", "_")
                new_path = os.path.join(root_dir, new_name)
                os.rename(path, new_path)
            else:
                new_name = filename.lower().replace(" ", "_").replace("-", "_")
                new_path = os.path.join(root_dir, new_name)
                os.rename(path, new_path)
        if depth == 0:
            print(f"Renamed all directories and files in {root_dir}")

    def move_items(self, items: list, src_dir: str, dest_dir: str) -> None:
        """
        Move items from a source directory to a destination directory.

        Raises:
            FileNotFoundError: If any expected item is never found under src_dir.
                The dataset archive layout may have changed; without this guard a
                missing item would be skipped silently and yield an empty database.
        """

        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        moved = set()
        for path, dirs, files in os.walk(src_dir):
            for item in items:
                if item in moved:
                    continue
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path) or item in files:
                    shutil.move(item_path, dest_dir)
                    moved.add(item)
                    print(f"Moved {item} from {src_dir} to {dest_dir}")
        missing = [item for item in items if item not in moved]
        if missing:
            raise FileNotFoundError(
                f"Expected item(s) not found under '{src_dir}': {missing}. "
                f"The dataset archive layout may have changed; verify the names "
                f"in deploy.py against the extracted contents."
            )

    def delete_directory(self, directory_path: str) -> None:
        """
        Delete a directory and its contents.
        """

        shutil.rmtree(directory_path)
        print(f"Deleted directory '{directory_path}'\n")

    def find_files(self, data_dir: str, ext: str) -> list:
        """
        Find all files with a specific extension in a directory.
        """

        csv_files = []
        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.endswith(ext):
                    csv_files.append(os.path.join(root, file))

        return csv_files
