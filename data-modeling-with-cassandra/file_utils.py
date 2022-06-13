
import os
import pandas as pd


class FileUtils:
    """
    Manage I/O files and directories, transform files to pandas dataframe and vice versa.
    """

    @staticmethod
    def get_directory_files_list(directory_path: str, file_ext: str):
        """
        Get all files with given extension in a given directory.
        :directory_path: path/to/directory.
        :file_ext: file extension.
        :return: list that contains all the paths to the files.
        """

        file_paths = []
        for root, _, files in os.walk(directory_path):
            file_paths.extend([os.path.join(root, file)
                              for file in files if file.endswith(file_ext)])

        return file_paths

    @staticmethod
    def file_num_rows(file_path: str) -> int:
        """
        Count the number of rows in a file.
        :param file_path: path/to/file.
        :return: number of lines in the file.
        """
        with open(file_path, 'r', encoding='utf8') as f:
            return sum(1 for _ in f)

    @staticmethod
    def read_file_to_pd(file_path: str, schema: dict):
        """ 
        Read a file into a pandas dataframe with a determined schema.
        
        Args:
            file_path (str): path/to/file
            schema (dict): desired schema of the pandas dataframe
        Returns:
            pandas.df: pandas dataframe
        """
        df = pd.read_csv(file_path)

        for k, v in schema.items():
            df[k] = df[k].astype(v)

        return df

    @staticmethod
    def files_to_pd(file_paths: list):
        """
        Read all the files of an array and makes append of all in only one pandas dataframe.
        :param file_path_list: array of files
        :return: pandas dataframe with all the files.
        """

        df_list = []

        for filename in file_paths:
            df = pd.read_csv(filename, index_col=None, header=0)
            df_list.append(df)

        return pd.concat(df_list, axis=0, ignore_index=True)

    @staticmethod
    def pd_to_file(file_path: str, df):
        """
        Writes a pandas dataframe in to a csv file.
        :param file_path: path/to/csv/file.
        :param df: pandas dataframe.
        """
        df.to_csv(file_path, sep=',', encoding='utf-8', header=1, index=False)
