import json
import re
from os import listdir
import os
import shutil
from datetime import datetime
import pandas as pd
from Logger.Logger import Applogger


class PredDatavalidation :
    """
    This class shall be ued for all the validation done on the Raw Prediction Data!!

    """

    def __init__(self, path):
        self.batch_directory = path
        self.schema_file = 'schema_prediction.json'
        self.logger = Applogger()



    def extract_values_from_schema(self):

        """
            Method Name : extract_values_from_schema
            Description : This method extracts all the relavant information from the pre defined 'SCHEMA' file.
            Output : LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName
            On Failure : Raise Exception

        """

        try :
            with open(self.schema_file, 'r') as f :

                schema_info = json.load(f)
                # f.close()
                len_DateStamp = schema_info['LengthOfDateStampInFile']
                len_TimeStamp = schema_info['LengthOfTimeStampInFile']
                num_Columns = schema_info['NumberofColumns']
                col_Name = schema_info['ColName']

            return len_DateStamp, len_TimeStamp, num_Columns, col_Name



        except Exception as e :
            raise e





    def manual_regex_creation(self):


        """
            Method Name: manual_regex_creation
            Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                         This Regex is used to validate the filename of the training data.
            Output: Regex pattern
            On Failure: None

        """
        file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
        try :

            regex = "['creditCardFraud']+['\_'']+[\d_]+[\d]+\.csv"
            self.logger.log(file, f'regex created for checking file name : {regex}')
            return regex

        except Exception as e:
            self.logger.log(file, f'error occured : {e}')
            file.close()
            raise e





    def create_dir_Good_Bad_raw_data(self):


        """
            Method Name: create_dir_for_good_raw_data
            Description: This method creates directories to store the Good Data and Bad Data after validating the training data.
            Output: None
            On Failure: raise error

        """

        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            path = os.path.join("Prediction_Raw_Files_Validated/", "Good_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join("Prediction_Raw_Files_Validated/", "Bad_Raw/")
            if not os.path.isdir(path):
                os.makedirs(path)

            self.logger.log(file, 'good bad for checking file name')

        except Exception as e:
            raise e



    def del_existing_good_data_folder(self):

        """
            Method Name: del_existing_good_data_folder
            Description: This method deletes the good training raw data folder after loading the data in the DB.
                         Once the good files are loaded in the DB, deleting the folder ensures space optimization.
            Output: None
            On Failure: raise error

        """
        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            path = "Prediction_raw_files_validated/"
            if os.path.isdir(path + 'Good_Raw'):
                shutil.rmtree(path + 'Good_Raw')

                message = 'Good_Raw folder deleted'
                self.logger.log(file, message)
                file.close()

        except Exception as e:
            raise e



    def del_existing_bad_data_folder(self):

        """
            Method Name: del_existing_bad_data_folder
            Description: This method deletes the bad training raw data folder after loading the data in the DB.
                         Once the good files are loaded in the DB, deleting the folder ensures space optimization.
            Output: None
            On Failure: raise error

        """
        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            path = "Prediction_raw_files_validated/"
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')

                self.logger.log(file, 'Bad_Raw folder deleted')
                file.close()



        except Exception as e:
            raise e



    def move_bad_files_to_archive(self):
        """
            Method Name : move_bad_files_to_archive
            Description : archive the bad files to send them back to the client for invalid data issue.
            Output : None
            On Faliure : Raise error

        """
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H%M%S')
        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            path = "PredictionArchivedBadData"

            if not os.path.isdir(path):
                os.makedirs(path)
            source = 'Prediction_raw_files_validated/Bad_Raw/'
            dest = 'PredictionArchivedBadData/BadData_' + str(date) + "_" + str(time)

            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f, dest)
            self.logger.log(file, "Bad files moved to archive")
            path = 'Prediction_raw_files_validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')
            self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")
            file.close()
        except Exception as e:
            raise e



    def raw_filename_validation(self, regex, len_DateStamp, len_TimeStamp):


        """

        Method Name : raw_file_validation
        Description :This function validates the name of the prediction csv files as per given name in the schema!
                     Regex pattern is used to do the validation.If name format do not match the file is moved
                     to Bad Raw Data folder else in Good raw data.
             Output : None
          On Failure: Raise Esception

        """
        file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
        self.del_existing_bad_data_folder()   # deleteing the exsisting good and bad folder in case of unsuccesful previous run
        self.del_existing_good_data_folder()
        self.create_dir_Good_Bad_raw_data()   # creating good and bad raw directory

        raw_filenames = [file for file in listdir(self.batch_directory)]   # storing all the filename in a list for validation
        try:
            for filename in raw_filenames:

                if (re.match(regex, filename)):
                    split_name = re.split('.csv', filename)
                    split_name = re.split('_', split_name[0])
                    if len(split_name[1]) == len_DateStamp:
                        if len(split_name[2]) == len_TimeStamp :
                            shutil.copy('Prediction_Batch_Files/' + filename, 'Prediction_raw_files_validated/Good_Raw/')
                            self.logger.log(file, f'{filename} copied into Good_Raw folder')
                        else:
                            shutil.copy('Prediction_Batch_Files/' + filename, 'Prediction_raw_files_validated/Bad_Raw/')
                            self.logger.log(file, f'{filename} copied into Bad_Raw folder')
                    else:
                        shutil.copy('Prediction_Batch_Files/' + filename, 'Prediction_raw_files_validated/Bad_Raw/')
                        self.logger.log(file, f'{filename} copied into Bad_Raw folder')
                else:
                    shutil.copy('Prediction_Batch_Files/' + filename, 'Prediction_raw_files_validated/Bad_Raw/')
                    self.logger.log(file, f'{filename} copied into Bad_Raw folder')

        except Exception as e :
            self.logger.log(file, f'Error occured : {e}')
            raise e
        file.close()



    def no_of_col_validation(self, num_Columns):

        """
            Method Name : no_of_col_validation
            Description: This method shall be used to validate the number of columns in the csv files, as per the Schema file.
                         if not, then the file will be moved to the bad raw folder.
            Output : None
            On Failure : Raise exception
        """
        f = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')


        try:
            self.logger.log(f, 'No of column validation started')
            self.good_raw_path = 'Prediction_raw_files_validated/Good_Raw/'

            for file in listdir(self.good_raw_path):
                csv = pd.read_csv(self.good_raw_path + file)
                if csv.shape[1] == num_Columns :
                    csv.rename(columns={'Unnamed: 0' : 'Wafer'}, inplace=True)
                    csv.to_csv("Prediction_raw_files_validated/Good_Raw/" + file, index=None, header=True)
                    pass
                else:
                    shutil.move('Prediction_raw_files_validated/Good_Raw/'+file, 'Prediction_raw_files_validated/Bad_Raw')
                    self.logger.log(f, f'{f} moved to Bad_Raw folder')

        except Exception as e:
            self.logger.log(f, f'error occured : {e}')
            raise e
        f.close()







    def null_col_validation(self):
        """
            Method Name : null_col_validation
            Description : This method shall be used for checking if a whole feature column is null or not.
                          If yes, then the file is not good for preprocessing, and that will be moved to bad raw folder.
            Output : None
            On Failure : Raise Exception

        """
        file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
        try:
            self.logger.log(file, 'Null column validation started')

            self.good_raw_path = 'Prediction_raw_files_validated/Good_Raw/'
            for goodfile in listdir(self.good_raw_path):
                count = 0
                df = pd.read_csv(self.good_raw_path + goodfile)
                for col in df:
                    if df[col].count() == 0 :
                        shutil.copy(self.good_raw_path + goodfile, 'Prediction_raw_files_validated/Bad_Raw')
                        self.logger.log(file, f'{goodfile} copied into Bad_Raw folder')
                        count = count + 1
                        break
                if count == 0:
                    df.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    df.to_csv('Prediction_raw_files_validated/Good_Raw/' + goodfile, index=None, header=True)

        except Exception as e:
            self.logger.log(file, f'error occured : {e}')
            raise e
        file.close()

    def deletePredictionFile(self):

        if os.path.exists('Prediction_Output_File/Predictions.csv'):
            os.remove('Prediction_Output_File/Predictions.csv')






