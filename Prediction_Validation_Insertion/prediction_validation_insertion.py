from Prediction_Raw_Data_Validation.prediction_raw_validation import PredDatavalidation
from DB_Operation.db_operation_prediction import DBOperationPrediction
from Transformation.prediction_transformation import DataTransformPrediction
from Logger.Logger import Applogger

class pred_validation:

    def __init__(self, path):

        self.raw_data = PredDatavalidation(path)

        self.db_operation = DBOperationPrediction()

        self.data_transform = DataTransformPrediction()

        self.logger = Applogger()



    def prediction_validation(self):

        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            self.logger.log(file, 'Raw data validation started !!')

            # extracting values from the schema file
            DateStamp_length, TimeStamp_length, num_of_Columns, col_Name = self.raw_data.extract_values_from_schema()
            self.logger.log(file, f'Values form schema extracted : DateStamp_length-{DateStamp_length}, TimeStamp_length-{TimeStamp_length}, num_of_Columns-{num_of_Columns}, col_Name-{col_Name} !!')
            self.logger.log(file, 'Data collected from schema')

            # getting the regex defined to validate the file name
            regex = self.raw_data.manual_regex_creation()
            self.logger.log(file, 'regex creation successful !!')



            # validating the raw file names
            self.raw_data.raw_filename_validation(regex, DateStamp_length, TimeStamp_length)
            self.logger.log(file, 'Raw data filename validation successful !!')

            # validating the number of columns in raw file
            self.raw_data.no_of_col_validation(num_of_Columns)
            self.logger.log(file, 'Raw data number of columns validation successful !!')

            # validating if there is a null column in the raw files
            self.raw_data.null_col_validation()
            self.logger.log(file, 'null column validation successful !!')

            # replacing the blanks in the file with 'NULL' to insert into the table
            self.data_transform.replace_missing_with_null()
            self.logger.log(file, 'Data transformation successful !!')

            self.logger.log(file, 'Raw data validation completed !!')

            # Database Operations
            self.logger.log(file, 'creating database and tables on the basis of schema!!')

            # creating database
            self.db_operation.create_table(db_name='PredictionDB', col_names=col_Name)
            self.logger.log(file, 'Database and table created!!')

            # inserting the data into the database
            self.db_operation.insert_good_data_into_table(db_name='PredictionDB')
            self.logger.log(file, 'data inserted into table successfully!!')


            # deleting existing good raw data folder
            self.raw_data.del_existing_good_data_folder()
            self.logger.log(file,'deleted exsisting Good_Raw folder successfully!!')

            # moving existing bad data folder to archive
            self.raw_data.move_bad_files_to_archive()
            self.logger.log(file, 'Bad_Raw files moved to archive successfully!!')

            # Exporting data from table into a csv file
            self.db_operation.export_data_from_table_into_final_csv(db_name='Training')
            self.logger.log(file, 'Data exported from db into csv file successfully!!')

            file.close()



        except Exception as e:
            raise e

