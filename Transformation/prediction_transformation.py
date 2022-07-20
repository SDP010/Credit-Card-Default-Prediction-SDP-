from os import listdir
import pandas as pd
from Logger.Logger import Applogger


class DataTransformPrediction:
    """
        This class shall be used for transforming the Good Raw Prediction Data before loading it in Database!!.
    """

    def __init__(self):
        self.good_data_path = 'Prediction_raw_files_validated/Good_Raw/'
        self.logger = Applogger()


    def replace_missing_with_null(self):

        """
            Method Name : replace_missing_with_Null
            Description : This function will replace all the missing values with "NULL".
            Output : None
            On Failure : Raise Exception

        """
        try:
            goodfiles = [file for file in listdir(self.good_data_path)]
            for file in goodfiles:
                df = pd.read_csv(self.good_data_path + file)
                df.fillna('NULL', inplace=True)
                df.to_csv(self.good_data_path + file, index=None, header=True)
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            self.logger.log(file, 'Replacing missing values with Null completed!!')

        except Exception as e:
            raise e
