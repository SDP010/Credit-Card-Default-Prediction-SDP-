import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from Logger.Logger import Applogger

class Preprocessor:
    """
        This class shall be used for cleaning and preprocessing the data before training.
    """

    def __init__(self):
        self.logger = Applogger()

    def remove_col(self, df, columns):
        """
            Method Name : remove_col
            Description: This method removes the given columns from a pandas dataframe.
            Output: A pandas DataFrame after removing the specified columns.
            On Failure: Raise Exception
        """
        self.df = df
        self.columns = columns

        try:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            useful_df = self.df.drop(columns=self.columns, axis=1)
            self.logger.log(file, 'Column removal Successful!!')
            file.close()
            return useful_df


        except Exception as e:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.logger.log(file, f'Error Ocurred : {e}')
            file.close()
            raise e

    def separate_label_feature(self, df, label_name):
        """
            Method Name: separate_label_feature
            Description: This method separates the features and a Label Coulmns.
            Output: Returns two separate Dataframes, one containing features and the other containing Labels .
            On Failure: Raise Exception
        """
        try:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.X = df.drop(label_name, axis= 1)
            self.Y = df[label_name]
            self.logger.log(file, 'Label and Feature separation successful!!')
            file.close()
            return self.X, self.Y

        except Exception as e:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.logger.log(file, f'Erroe Occured : {e}')
            file.close()
            return e

    def is_null_present(self, df):
        """
            Method Name: is_null_present
            Description: This method checks whether there are null values present in the pandas Dataframe or not.
            Output: Returns a Boolean Value. True if null values are present in the DataFrame, False if they are not present.
            On Failure: Raise Exception

        """
        self.null_present = False
        try:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.null_count = df.isna().sum()    # count of the null values per column
            for i in self.null_count:
                if i > 0:
                    self.null_present = True
                    self.logger.log(file, 'Null values exist!!')
                    break

            self.logger.log(file, 'Null values checking successful!!')
            file.close()
            return self.null_present

        except Exception as e:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.logger.log(file, f'Erroe Occured : {e}')
            file.close()
            raise e


    def impute_missing_values(self, df):
        """
            Method Name: impute_missing_values
            Description: This method replaces all the missing values in the Dataframe using KNN Imputer.
            Output: A Dataframe which has all the missing values imputed.
            On Failure: Raise Exception
        """
        self.df = df
        try:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            imputer = KNNImputer(n_neighbors=3, weights='uniform', missing_values=np.nan)
            self.new_array = imputer.fit_transform(self.df)  # impute the missing values

            # COVERTING THE nd ARRAY RETURNED IN THE ABOVE STEP INTO A DATAFRAME
            self.new_df = pd.DataFrame(data=self.new_array, columns=self.df.columns)
            self.logger.log(file, 'Missing values imputation successful!!')
            file.close()
            return self.new_df

        except Exception as e:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.logger.log(file, f'Erroe Occured : {e}')
            file.close()
            raise e

    def get_columns_with_zero_std_deviation(self,df):
        """
            Method Name: get_columns_with_zero_std_deviation
            Description: This method finds out the columns which have a standard deviation of zero.
            Output: List of the columns with standard deviation of zero
            On Failure: Raise Exception
        """
        self.columns = df.columns
        self.df_details = df.describe()
        self.col_to_drop = []
        try:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            for i in self.columns:
                if (self.df_details[i]['std'] == 0):
                    self.col_to_drop.append(i)
                    self.logger.log(file,f'{i} coloumn has zero std deviation!!')
            file.close()
            return self.col_to_drop

        except Exception as e:
            file = open('Logs/Preprocessing_log.txt', 'a+')
            self.logger.log(file, f'Erroe Occured : {e}')
            file.close()
            raise e












