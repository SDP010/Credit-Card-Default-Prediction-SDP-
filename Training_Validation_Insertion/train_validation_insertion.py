from Logger.Logger import Applogger
from Training_Raw_Data_Validation.training_raw_validation import RawDataValidation
from Transformation.training_transformation import DataTransformTraining
from DB_Operation.db_operation_training import DBOperation


class train_validation:

    def __init__(self, path):
        self.raw_data = RawDataValidation(path)
        self.db_operation = DBOperation()
        self.data_transform = DataTransformTraining()
        self.path = path
        self.logger = Applogger()

    def train_validation(self):

        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')

            # RAW DATA VALIDATION
            self.logger.log(file, 'Raw data validation started !!')

            # extracting values from the schema file
            DateStamp_length, TimeStamp_length, num_of_Columns, col_Name = self.raw_data.extract_values_from_schema()
            self.logger.log(file, f'Values form schema extracted : DateStamp_length-{DateStamp_length}, TimeStamp_length-{TimeStamp_length}, num_of_Columns-{num_of_Columns}, col_Name-{col_Name} !!')

            # getting the regex defined to validate the file name
            regex = self.raw_data.manual_regex_creation()
            self.logger.log(file, 'Regex created for raw data filename validation !!')

            # validating the raw file names
            self.raw_data.raw_filename_validation(regex, DateStamp_length, TimeStamp_length)
            self.logger.log(file, 'Raw data filename validation successful !!')

            # validating the number of columns in raw file
            self.raw_data.no_of_col_validation(num_of_Columns)
            self.logger.log(file, 'Number of column in raw file validation successfully !!')

            # validating if there is a null column in the raw files
            self.raw_data.null_col_validation()
            self.logger.log(file, 'Null column validation successful!!')

            # replacing the blanks in the file with 'NULL' to insert into the table

            self.data_transform.replace_missing_with_null()
            self.logger.log(file, 'Replacing missing values with "NULL" successful !!')

            self.logger.log(file, 'Raw data validation complete !!')

            # DATABASE OPERATIONS

            # creating database
            self.db_operation.create_table(db_name='TrainingDB', col_names=col_Name)
            self.logger.log(file, 'Table created successfully !!')

            # inserting the data into the database
            self.db_operation.insert_good_data_into_table(db_name='TrainingDB')
            self.logger.log(file, 'Data insertion in table completed !!')

            # deleting existing good raw data folder
            self.raw_data.del_existing_good_data_folder()
            self.logger.log(file, 'Existing good raw data folder deleted !!')

            # moving existing bad data folder to archive
            self.raw_data.move_bad_files_to_archive()
            self.logger.log(file, 'Bad raw data moved to archive successfully !!')

            # Exporting data from table into a csv file
            self.db_operation.export_data_from_table_into_final_csv(db_name='TrainingDB')
            self.logger.log(file, 'Good raw data for training exported from database to csv file !!')

            file.close()

        except Exception as e :
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            self.logger.log(file, f'Error occured : {e} !!')
            file.close()
            raise e