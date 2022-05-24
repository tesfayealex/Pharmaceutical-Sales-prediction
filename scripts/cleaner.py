import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer


class CleanDataFrame:

    @staticmethod
    def get_numerical_columns(df: pd.DataFrame) -> list:
        numerical_columns = df.select_dtypes(include='number').columns.tolist()
        return numerical_columns

    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> list:
        categorical_columns = df.select_dtypes(
            include=['object']).columns.tolist()
        return categorical_columns

    def fix_datatypes(self, df: pd.DataFrame, column: str = None, to_type: type = None) -> pd.DataFrame:
        """
        Takes in the sales dataframe an casts columns to proper data type
        """
        datetime_columns = ['Date']
        string_columns = ['PromoInterval','StoreType','Assortment']
        df_columns = df.columns
        for col in string_columns:
            if col in df_columns:
                df[col] = df[col].astype("string")
        for col in datetime_columns:
            if col in df_columns:
                df[col] = pd.to_datetime(df[col])
        if column and to_type:
            df[column] = df[column].astype(to_type)

        return df

    def percent_missing(self, df):
        """
        Print out the percentage of missing entries in a dataframe
        """
        # Calculate total number of cells in dataframe
        totalCells = np.product(df.shape)

        # Count number of missing values per column
        missingCount = df.isnull().sum()

        # Calculate total number of missing values
        totalMissing = missingCount.sum()

        # Calculate percentage of missing values
        print("The dataset contains", round(
            ((totalMissing/totalCells) * 100), 2), "%", "missing values.")

    def get_mct(self, series: pd.Series, measure: str):
        """
        get mean, median or mode depending on measure
        """
        measure = measure.lower()
        if measure == "mean":
            return series.mean()
        elif measure == "median":
            return series.median()
        elif measure == "mode":
            return series.mode()[0]

    def replace_missing(self, df: pd.DataFrame, columns: str, method: str) -> pd.DataFrame:

        for column in columns:
            nulls = df[column].isnull()
            indecies = [i for i, v in zip(nulls.index, nulls.values) if v]
            replace_with = self.get_mct(df[column], method)
            df.loc[indecies, column] = replace_with

        return df
    def fix_missing_values(self,df:pd.DataFrame,columns: list,value) -> pd.DataFrame:
        for column in columns:
            df[column] = df[column].fillna(value)
        return df


    def remove_null_row(self, df: pd.DataFrame, columns: str) -> pd.DataFrame:
        for column in columns:
            df = df[~ df[column].isna()]
        return df

    def normal_scale(self, df: pd.DataFrame) -> pd.DataFrame:
        scaller = StandardScaler()
        scalled = pd.DataFrame(scaller.fit_transform(
            df[self.get_numerical_columns(df)]))
        scalled.columns = self.get_numerical_columns(df)

        return scalled

    def minmax_scale(self, df: pd.DataFrame) -> pd.DataFrame:
        scaller = MinMaxScaler()
        scalled = pd.DataFrame(
            scaller.fit_transform(
                df[self.get_numerical_columns(df)]),
            columns=self.get_numerical_columns(df)
        )

        return scalled

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        normalizer = Normalizer()
        normalized = pd.DataFrame(
            normalizer.fit_transform(
                df[self.get_numerical_columns(df)]),
            columns=self.get_numerical_columns(df)
        )

        return normalized

    def drop_duplicates(self, df: pd.DataFrame , subset=None) -> pd.DataFrame:
        """
        This checkes if there are any duplicated entries for a user
        And remove the duplicated rows
        """
        if subset == None:
            df = df.drop_duplicates(subset='')
        else:
             df = df.drop_duplicates()
        return df

    def drop_columns(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Drops columns that are not essesntial for modeling
        """
        if len(columns) != 0:
            df.drop(columns=columns, inplace=True)
        return df

    def run_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This runs a series of cleaner methods on the df passed to it. 
        """
        df = self.drop_duplicates(df)
        df = self.drop_columns(df)
        df.reset_index(drop=True, inplace=True)

        return df
