from os import listdir
import pandas as pd
from Logger.Logger import Applogger

class DataTransformTraining:
    """
        This class shall be used for transforming the Good Raw Training Data before loading it in Database!!.
    """

    def __init__(self):
        self.good_data_path = 'Training_raw_files_validated/Good_Raw/'
        # self.good_data_path = 'Training_Raw_File/'
        self.logger = Applogger()

    def replace_missing_with_null(self):

        """
            Method Name : replace_missing_with_Null
            Description : This function will replace all the missing values with "NULL".
            Output : None
            On Failure : Raise Exception

        """
        f = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            self.logger.log(f, 'Replacing missing values with "NULL" !!')
            all_files = [file for file in listdir(self.good_data_path)]
            for file in all_files:
                df = pd.read_csv(self.good_data_path + file)
                df.fillna('NULL', inplace=True)
                df.to_csv(self.good_data_path + file, index=None, header=True)

            self.logger.log(f, 'Replaced missing values with "NULL" !!')

        except Exception as e:
            self.logger.log(f, f'Error occurred : {e}!!')
            f.close()
            raise e




