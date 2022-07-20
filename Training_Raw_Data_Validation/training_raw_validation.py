import json
import re
from os import listdir
import os
import shutil
from datetime import datetime
import pandas as pd
from Logger.Logger import Applogger   # custom module

class RawDataValidation :

    """

    This class shall be ued for all the validation done on the Raw Trainnig Data!!

    """

    def __init__(self, path):
        self.batch_directory = path
        self.schema_file = 'schema_training.json'
        self.logger = Applogger()


    def extract_values_from_schema(self):

        """
            Method Name : extract_values_from_schema
            Description : This method extracts all the relavant information from the pre defined 'SCHEMA' file.
            Output : LengthOfDateStampInFile, LengthOfTimeStampInFile, NumberofColumns, ColName
            On Failure : Raise Exception

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try :
            with open('schema_training.json', 'r') as f :
                schema_info = json.load(f)
                f.close()
                len_DateStamp = schema_info['LengthOfDateStampInFile']
                len_TimeStamp = schema_info['LengthOfTimeStampInFile']
                num_Columns = schema_info['NumberofColumns']
                col_Name = schema_info['ColName']
                self.logger.log(file, 'Information extracted from schema successfully !!')
                return len_DateStamp, len_TimeStamp, num_Columns, col_Name
        except Exception as e :
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e

        # return len_DateStamp, len_TimeStamp, num_Columns, col_Name


    def manual_regex_creation(self):

        """
            Method Name: manual_regex_creation
            Description: This method contains a manually defined regex based on the "FileName" given in "Schema" file.
                         This Regex is used to validate the filename of the training data.
            Output: Regex pattern
            On Failure: None

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try :
            regex = "['creditCardFraud']+['\_'']+[\d_]+[\d]+\.csv"
            self.logger.log(file, 'Manual regex created successfully')
            return regex

        except Exception as e:
            self.logger.log(file, f'Error Occurred wile creating regex : {e} !!')
            file.close()
            raise e



    def create_dir_Good_Bad_raw_data(self):

        """
            Method Name: create_dir_for_good_raw_data
            Description: This method creates directories to store the Good Data and Bad Data after validating the training data.
            Output: None
            On Failure: raise error

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            path = os.path.join('Training_raw_files_validated/' + 'Good_Raw')
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join('Training_raw_files_validated/' + 'Bad_Raw')
            if not os.path.isdir(path):
                os.makedirs(path)

            self.logger.log(file, 'good bad folder created for checking file name')


        except Exception as e :
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e


    def del_existing_good_data_folder(self):

        """
            Method Name: del_existing_good_data_folder
            Description: This method deletes the good training raw data folder after loading the data in the DB.
                         Once the good files are loaded in the DB, deleting the folder ensures space optimization.
            Output: None
            On Failure: raise error

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            path = "Training_raw_files_validated/"
            if os.path.isdir(path + 'Good_Raw'):
                shutil.rmtree(path + 'Good_Raw')

            self.logger.log(file, 'Good_Raw folder deleted')

        except Exception as e:
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e


    def del_existing_bad_data_folder(self):

        """
            Method Name: del_existing_bad_data_folder
            Description: This method deletes the bad training raw data folder after loading the data in the DB.
                         Once the good files are loaded in the DB, deleting the folder ensures space optimization.
            Output: None
            On Failure: raise error

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            path = "Training_raw_files_validated/"
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')

            self.logger.log(file, 'Bad_Raw folder deleted')

        except Exception as e:
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e

    def move_bad_files_to_archive(self):
        """
            Method Name : move_bad_files_to_archive
            Description : archive the bad files to send them back to the client for invalid data issue.
            Output : None
            On Faliure : Raise error

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        now = datetime.now()
        date = now.date()
        time = now.strftime('%H%M%S')
        try:
            path = "TrainingArchivedBadData"
            if not os.path.isdir(path):
                os.makedirs(path)

            source = 'Training_raw_files_validated/Bad_Raw/'
            dest = 'TrainingArchivedBadData/BadData_' + str(date) + "_" + str(time)

            if not os.path.isdir(dest):
                os.makedirs(dest)
            files = os.listdir(source)
            for f in files:
                if f not in os.listdir(dest):
                    shutil.move(source + f, dest)

            self.logger.log(file, "Bad files moved to archive")

            path = 'Training_raw_files_validated/'
            if os.path.isdir(path + 'Bad_Raw/'):
                shutil.rmtree(path + 'Bad_Raw/')

            self.logger.log(file, "Bad Raw Data Folder Deleted successfully!!")

        except Exception as e :
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e


    def raw_filename_validation(self, regex, len_DateStamp, len_TimeStamp):

        """

        Method Name : raw_file_validation
        Description :This function validates the name of the training csv files as per given name in the schema!
                     Regex pattern is used to do the validation.If name format do not match the file is moved
                     to Bad Raw Data folder else in Good raw data.
             Output : None
          On Failure: Raise Esception

        """

        file = open('Logs/Training_Logs/training_log.txt', 'a+')

        # deleteing the exsisting good and bad folder in case of unsuccesful previous run
        self.del_existing_bad_data_folder()
        self.del_existing_good_data_folder()
        self.create_dir_Good_Bad_raw_data()  # creating good bad raw folder
        # storing all the filename in a list for validation
        raw_filenames = [file for file in listdir(self.batch_directory)]

        try:
            for filename in raw_filenames:
                if (re.match(regex, filename)) :
                    split_name = re.split('.csv', filename)
                    split_name = re.split('_', split_name[0])
                    if len(split_name[1]) == len_DateStamp:
                        if len(split_name[2]) == len_TimeStamp :
                            shutil.copy('Training_Batch_Files/' + filename, 'Training_raw_files_validated/Good_Raw')
                            self.logger.log(file, f'{filename} copied into Good_Raw folder')
                        else:
                            shutil.copy('Training_Batch_Files/' + filename, 'Training_raw_files_validated/Bad_Raw')
                            self.logger.log(file, f'{filename} copied into Bad_Raw folder')
                    else:
                        shutil.copy('Training_Batch_Files/' + filename, 'Training_raw_files_validated/Bad_Raw')
                        self.logger.log(file, f'{filename} copied into Bad_Raw folder')
                else:
                    shutil.copy('Training_Batch_Files/' + filename, 'Training_raw_files_validated/Bad_Raw')
                    self.logger.log(file, f'{filename} copied into Bad_Raw folder')

        except Exception as e :
            self.logger.log(file, f'Error Occurred: {e} !!')
            file.close()
            raise e


    def no_of_col_validation(self, num_Columns):
        """
            Method Name : no_of_col_validation
            Description: This method shall be used to validate the number of columns in the csv files, as per the Schema file.
                         if not, then the file will be moved to the bad raw folder.
            Output : None
            On Failure : Raise exception
        """

        f = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            self.good_raw_path = 'Training_raw_files_validated/Good_Raw/'

            for file in listdir(self.good_raw_path):
                csv = pd.read_csv(self.good_raw_path + file)
                if csv.shape[1] == num_Columns :
                    csv.rename(columns={'Unnamed: 0': 'Wafer'}, inplace=True)
                    csv.to_csv("Training_raw_files_validated/Good_Raw/" + file, index=None, header=True)
                    pass
                else:
                    shutil.move('Training_raw_files_validated/Good_Raw/'+file, 'Training_raw_files_validated/Bad_Raw')
                    self.logger.log(f, f'{file} moved to Bad_Raw folder')

        except Exception as e:
            self.logger.log(f, f'Error Occurred: {e} !!')
            f.close()
            raise e


    def null_col_validation(self):
        """
            Method Name : null_col_validation
            Description : This method shall be used for checking if a whole feature column is null or not.
                          If yes, then the file is not good for preprocessing, and that will be moved to bad raw folder.
            Output : None
            On Failure : Raise Exception

        """
        file = open('Logs/Training_Logs/training_log.txt', 'a+')
        try:
            self.logger.log(file, 'Null column validation started')

            self.good_raw_path = 'Training_raw_files_validated/Good_Raw/'
            # self.good_raw_path = 'Training_Raw_File/'
            for goodfile in listdir(self.good_raw_path):
                count = 0
                df = pd.read_csv(self.good_raw_path + goodfile)
                for col in df:
                    if df[col].count() == 0:
                        shutil.copy(self.good_raw_path + goodfile, 'Training_raw_files_validated/Bad_Raw')
                        self.logger.log(file, f'{goodfile} copied into Bad_Raw folder')
                        count = count + 1
                        break
                if count == 0:
                    df.rename(columns={"PAY_0": "PAY_1"}, inplace=True)
                    df.to_csv('Training_raw_files_validated/Good_Raw/' + goodfile, index=None, header=True)

        except Exception as e:
                self.logger.log(file, f'Error Occurred: {e} !!')
                file.close()
                raise e

