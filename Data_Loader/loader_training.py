import pandas as pd
from Logger.Logger import Applogger

class Data_loader:
    """
        This class should be used for loadig the preprocessed training data from the directory
    """

    def __init__(self):
        self.training_file = 'Training_file_fromdb/Training_Input_file.csv'
        self.logger = Applogger()


    def get_data(self):
        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            df = pd.read_csv(self.training_file)
            self.logger.log(file, 'training data loaded sucessfully!!')
            return df
        except Exception as e:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            self.logger.log(file, f'Error Occured : {e}')
            raise e