import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, Normalizer
from logger import logger


class CleanDataFrame:

    @staticmethod
    def get_numerical_columns(df: pd.DataFrame) -> list:
        try:
            numerical_columns = df.select_dtypes(include='number').columns.tolist()
            logger.info('successfully got numerical columns')
            return numerical_columns
        except Exception as e:
            logger.error(e)
            return []
        

    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> list:
        try:
            categorical_columns = df.select_dtypes(
                include=['object']).columns.tolist()
            logger.info('successfully got catagorical columns')
            return categorical_columns
        except Exception as e:
            logger.error(e)
            return []
       

    def fix_datatypes(self, df: pd.DataFrame, column: str = None, to_type: type = None) -> pd.DataFrame:
        """
        Takes in the sales dataframe an casts columns to proper data type
        """
        try:
            datetime_columns = ['Date']
            string_columns = ['PromoInterval',
                            'StoreType', 'Assortment', 'StateHoliday']
            int_columns = ['CompetitionOpenSinceYear',
                        'CompetitionOpenSinceMonth', 'Promo2SinceWeek', 'Promo2SinceYear']
            df_columns = df.columns
            for col in string_columns:
                if col in df_columns:
                    df[col] = df[col].astype("string")
                logger.info(f'successfully changed {col} column to string')
            for col in datetime_columns:
                if col in df_columns:
                    df[col] = pd.to_datetime(df[col])
                logger.info(f'successfully changed {col} column to datetime')
            for col in int_columns:
                if col in df_columns:
                    df[col] = df[col].astype("int64")
                logger.info(f'successfully changed {col} column to integer')
            if column and to_type:
                df[column] = df[column].astype(to_type)
                logger.info(f'successfully changed {col} column to {to_type}')
            logger.info('successfully finished fixing datatype')
        except Exception as e:
            logger.error(e)
        return df

    def percent_missing(self, df):
        """
        Print out the percentage of missing entries in a dataframe
        """
        try:
            # Calculate total number of cells in dataframe
            totalCells = np.product(df.shape)

            # Count number of missing values per column
            missingCount = df.isnull().sum()

            # Calculate total number of missing values
            totalMissing = missingCount.sum()

            # Calculate percentage of missing values
            logger.info(
                f"The dataset contains {round(((totalMissing/totalCells) * 100), 2)} % missing values.")
        except Exception as e:
            logger.error(e)

    def get_mct(self, series: pd.Series, measure: str):
        """
        get mean, median or mode depending on measure
        """
        try:
            measure = measure.lower()
            if measure == "mean":
                return series.mean()
            elif measure == "median":
                return series.median()
            elif measure == "mode":
                return series.mode()[0]
        except Exception as e:
            logger.error(e)
             
    def replace_missing(self, df: pd.DataFrame, columns: str, method: str) -> pd.DataFrame:
        try:
            for column in columns:
                nulls = df[column].isnull()
                indecies = [i for i, v in zip(nulls.index, nulls.values) if v]
                replace_with = self.get_mct(df[column], method)
                df.loc[indecies, column] = replace_with
                logger.info(
                    f'successfully replaced missing values of {column} column with {method} method')
        except Exception as e:
            logger.error(e)
        return df
        

    def fix_missing_values(self, df: pd.DataFrame, columns: list, value) -> pd.DataFrame:
        try:
            for column in columns:
                df[column] = df[column].fillna(value)
                logger.info(
                    f'successfully fixed missing values of {column} column with {value}')
        except Exception as e:
            logger.error(e)
        return df

    def replace_value(self, df: pd.DataFrame, column, val_before, val_to):
        try:
            df.loc[df[column] == val_before, column] = val_to
            logger.info(
                f'successfully replaced value of {column} column with {val_to}')
        except Exception as e:
            logger.error(e)
        return df

    def remove_null_row(self, df: pd.DataFrame, columns: str) -> pd.DataFrame:
        try:
            for column in columns:
                df = df[~ df[column].isna()]
                logger.info(
                    f'successfully removed empty rows with null {column} column')
        except Exception as e:
            logger.error(e)
        return df

    def normal_scale(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            scaller = StandardScaler()
            scalled = pd.DataFrame(scaller.fit_transform(
                df[self.get_numerical_columns(df)]))
            scalled.columns = self.get_numerical_columns(df)
            logger.info(f'successfully scalled the dataframe')
            return scalled
        except Exception as e:
            logger.error(e)
            return df
        

    def minmax_scale(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            scaller = MinMaxScaler()
            scalled = pd.DataFrame(
                scaller.fit_transform(
                    df[self.get_numerical_columns(df)]),
                columns=self.get_numerical_columns(df)
            )

            return scalled
        except Exception as e:
            logger.error(e)
            return df

    def normalize(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            normalizer = Normalizer()
            normalized = pd.DataFrame(
                normalizer.fit_transform(
                    df[self.get_numerical_columns(df)]),
                columns=self.get_numerical_columns(df)
            )
            logger.info(f'successfully normalized dataframe')
            return normalized
        except Exception as e:
            logger.error(e)
            return df

    def drop_duplicates(self, df: pd.DataFrame, subset=None) -> pd.DataFrame:
        """
        This checkes if there are any duplicated entries for a user
        And remove the duplicated rows
        """
        try:
            if subset != None:
                df = df.drop_duplicates(subset='')
            else:
                df = df.drop_duplicates()
            logger.info(f'successfully droped duplicates')
        except Exception as e:
            logger.error(e)
        return df

    def drop_columns(self, df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """
        Drops columns that are not essesntial for modeling
        """
        try:
            if len(columns) != 0:
                df.drop(columns=columns, inplace=True)
            logger.info(f'successfully dropped columns')
        except Exception as e:
            logger.error(e)
        return df

    def run_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This runs a series of cleaner methods on the df passed to it. 
        """
        try:
            df = self.drop_duplicates(df)
            # df = self.drop_columns(df)
            df.reset_index(drop=True, inplace=True)
            logger.info(f'successfully finished cleaning pipeline')
        except Exception as e:
            logger.error(e)
        return df
