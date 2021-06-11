import logging
import pandas as pd
import sys
from multiprocessing import Pool
from pathlib import Path
import os

sys.path.insert(0, "..")  # just to have consistent imports in scripts and notebooks
from russian_trolls.tweets_preprocessor import TweetsPreprocessor


class ExternalDatasetCreator:
    def __init__(self, raw_input_data_dir: str):
        """
        This class provides functionality of creating a preprocessed csv file out of raw blob downloaded with
        download_data.sh script
        Args:
            raw_input_data_dir: directory where the raw twitter stream is held f.e. '../data/twitter-stream/2017/09/10'
        """
        self.raw_input_data_dir = raw_input_data_dir

    def load_and_preprocess_single_file(self, file_path: str) -> pd.DataFrame:
        """
        Loads and preprocess data from a compressed raw tweets jsons to dataframe.
        Preprocessing includes:
            - removing not used columns
            - cleaning up the text
            - detecting and preserving only english tweets
        Args:
            file_path: path to a file to be loaded
        Returns:
            preprocessed dataframe
        """
        df = pd.read_json(file_path, compression="bz2", lines=True)[
            ["id", "created_at", "text", "retweet_count"]
        ].dropna()
        df["text_clean"] = df["text"].map(lambda x: TweetsPreprocessor.cleaner(x))
        df["language"] = df["text"].map(
            lambda x: TweetsPreprocessor.detect_language_or_null(x)
        )
        df = df[df["language"] == "en"]
        return df

    def generate_dataset(
        self, output_file: str, max_number_of_raw_files_to_load: int = 40
    ):
        """
        Performs loading and preprocessing data from raw, compressed json with tweets into a csv file.
        Args:
            output_file: output csv file path
            max_number_of_raw_files_to_load: limit of files to be loaded
        """

        logging.info(f"Loading & preprocessing files from {self.raw_input_data_dir}")
        files = list(Path(self.raw_input_data_dir).rglob("*.bz2"))
        files.sort()

        with Pool(3) as p:
            dataframes = p.map(
                self.load_and_preprocess_single_file,
                files[:max_number_of_raw_files_to_load],
            )
        df = pd.concat(dataframes)
        df["is_troll"] = False

        logging.info(f"Saving preprocessed tweets to:{output_file}")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)


class TrollsDatasetCreator:
    def __init__(self, raw_input_data_csv: str):
        """
        This class provides functionality of creating a preprocessed csv file out of provided raw twieets csv
        Args:
            raw_input_data_csv: directory where the raw trolls twittees is held f.e. '../data/provided_offline/tweets.csv'
        """
        self.raw_input_data_csv = raw_input_data_csv

    def generate_dataset(self, output_file: str):
        """
        Performs loading and preprocessing data and places result into a csv file.
        TODO: This method is slow, pandas operations could be made parallel with f.e. modin or dask
        Args:
            output_file: output csv file path
            max_number_of_raw_files_to_load: limit of files to be loaded
        """

        logging.info(f"Loading & preprocessing data from {self.raw_input_data_csv}")
        logging.warning(
            f"This method is not yet optimised for speed, it can take up to 10 minutes!"
        )

        df = pd.read_csv(self.raw_input_data_csv)[
            ["tweet_id", "created_at", "text", "retweet_count"]
        ]
        df = df.sample(1000)
        df = df.rename(columns={"tweet_id": "id"})
        df["created_at"] = pd.to_datetime(df["created_at"], unit="ms")
        df["retweet_count"] = df.retweet_count.fillna(0)

        df["text_clean"] = df["text"].map(lambda x: TweetsPreprocessor.cleaner(x))
        df["language"] = df["text"].map(
            lambda x: TweetsPreprocessor.detect_language_or_null(x)
        )
        df = df[df["language"] == "en"]
        df["is_troll"] = True

        logging.info(f"Saving preprocessed tweets to:{output_file}")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)


if __name__ == "__main__":
    external_data_dir = "../data/twitter-stream/2017/09/10"
    non_trolls_output_file = "../data/preprocessed/non_trolls.csv"
    ds_creator = ExternalDatasetCreator(external_data_dir)
    ds_creator.generate_dataset(non_trolls_output_file, 400)

    provided_data_file = "../data/provided_offline/tweets.csv"
    trolls_output_file = "../data/preprocessed/trolls.csv"
    trolls_ds_creator = TrollsDatasetCreator(provided_data_file)
    trolls_ds_creator.generate_dataset(trolls_output_file)

    df = pd.concat(
        [
            pd.read_csv(non_trolls_output_file),
            pd.read_csv(trolls_output_file),
        ]
    )
    df.to_csv("../data/dataset.csv", index=False)
