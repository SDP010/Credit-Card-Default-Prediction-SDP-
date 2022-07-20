import csv
import shutil
import mysql.connector as connection
from Logger.Logger import Applogger
import os
from os import listdir

class DBOperation:
    """
            This class shall be used for handling all the SQL operation for training
    """

    def __init__(self):
        self.path = 'Training_Database/'
        self.good_file_path = 'Training_raw_files_validated/Good_Raw/'
        self.bad_file_path = 'Training_raw_files_validated/Bad_Raw/'
        self.logger = Applogger()



    def db_connector(self,db_name):
        """
            Method Name : db_connector
            Description : This method creates the database with the given name and
                          if Database already exists then opens the connection to the DB.
            Output : database connection
            On Failure : Raise exception
        """

        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            conn = connection.connect(host='localhost', user='root', passwd='Subhra@1234')
            self.logger.log(file, 'Connection to the server established successfully !!')
            cursor = conn.cursor()

            try:
                cursor.execute(f'create database {db_name}')
                cursor.execute(f'use {db_name}')
            except:
                cursor.execute(f'use {db_name}')

            self.logger.log(file, 'Database created and connected successfully !!')
            file.close()

        except Exception as e:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            self.logger.log(file, f'Error Ocured : {e}')
            file.close()
            raise e
        return conn



    def create_table(self, db_name, col_names):
        """
           Method Name : create_table
           Description : This method creates a table in the given database which will be used for
                         inserting the good raw training data.
           Output : None
           On Failure : Raise exception

        """

        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            conn = self.db_connector(db_name=db_name)
            cursor = conn.cursor()
            cursor.execute(f'use {db_name}')
            cursor.execute('drop table if exists Good_Raw_Data')
            for key in col_names:
                type = col_names[key]
                key1 = key.replace(' ','_')

                try:
                    cursor.execute(f'create table Good_Raw_Data ({key1} {type}(30))')
                    self.logger.log(file, 'create table Good_Raw_Dataa!!')
                except:
                    cursor.execute(f'alter table Good_Raw_Data add ({key1} {type}(30))')
                    self.logger.log(file, 'alter table Good_Raw_Dataa!!')

            self.logger.log(file, 'Table created for prediction data successfully!!!')
            conn.commit()
            conn.close()
            file.close()

        except Exception as e :
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            self.logger.log(file, f'Error Ocured : {e}')
            file.close()
            raise e




    def insert_good_data_into_table(self, db_name):
        """
            Method Name : insert_good_data_into_table
            Description : This method inserts the good raw training data from the folder
                          inside the given database.
            Output : None
            On Failure : Raise Exception

        """
        file1 = open('Logs/Training_Logs/training_log.txt', 'a+')
        conn = self.db_connector(db_name= db_name)
        cursor = conn.cursor()
        good_file_path = self.good_file_path
        onlyfiles = [file for file in listdir(good_file_path)]
        try :
            for file in onlyfiles :
                try:
                    with open(good_file_path + file) as f :
                        next(f)
                        reader = csv.reader(f, delimiter='\n')
                        for line in enumerate(reader):
                            for l in line[1]:
                                try:
                                    cursor.execute(f'insert into Good_Raw_Data values ({l})')
                                    conn.commit()
                                except Exception as e :
                                    raise e
                    self.logger.log(file1, f'{file} loaded to database sucessfully!!')

                except Exception as e:
                    self.logger.log(file1, f'Error Ocured : {e}')
                    raise e

        except Exception as e:
            self.logger.log(file1, f'Error Ocured : {e}')
            conn.close()
            raise e
        file1.close()


    def export_data_from_table_into_final_csv(self, db_name):
        """
            Method Name : export_data_from_table_into_final_csv
            Description : This method exports the good data into a csv file.
            Output : None
            On Failure : Raise exception

        """
        self.file_fromdb = 'Training_file_fromdb/'
        self.file_name = 'Training_Input_file.csv'

        try:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            conn = self.db_connector(db_name=db_name)
            cursor = conn.cursor()
            cursor.execute('use TrainingDB')
            cursor.execute('select * from Good_Raw_Data')
            result = cursor.fetchall()
            self.logger.log(file, 'Data fetched database!!!')

            headers = [i[0] for i in cursor.description]   # get the headers of the csv file

            # MAKING DIRECTORY FOR THE OUTPUT CSV FILE
            if not os.path.isdir(self.file_fromdb):
                os.makedirs(self.file_fromdb)

            # OPENING CSV FILE FOR WRITING
            self.logger.log(file, 'Writing data into csv file !!!')
            csv_file = csv.writer(open(self.file_fromdb + self.file_name, 'w', newline=''), delimiter=',')
            csv_file.writerow(headers)
            csv_file.writerows(result)
            conn.close()
            self.logger.log(file, 'Data successfully exported into csv file !!!')
            file.close()

        except Exception as e:
            file = open('Logs/Training_Logs/training_log.txt', 'a+')
            self.logger.log(file, f'Error Ocured : {e}')
            file.close()
            raise e