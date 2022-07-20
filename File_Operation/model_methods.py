import pickle
import os
from Logger.Logger import Applogger

class model_operations:
    """
        This class shall be used for saving, loading the model after training and also for
        finding the correct model for each cluster in time of prediction.
    """

    def __init__(self):
        self.logger = Applogger()

    def save_model(self, model, file_name):
        """
            Method Name: save_model
            Description: Save the model file to directory
            Outcome: File gets saved
            On Failure: Raise Exception
        """
        try:
            file = open('Logs/Model_operations_log.txt', 'a+')
            path = os.path.join('models/' + file_name)
            if not os.path.isdir('models/'):
                os.mkdir('models/')
            with open(path + '.pkl', 'wb') as f:
                pickle.dump(model, f)
            self.logger.log(file, 'the model saved into file {}'.format(file_name))
            file.close()
        except Exception as e:
            file = open('Logs/Model_operations_log.txt', 'a+')
            self.logger.log(file, f'Error occured : {e}')
            file.close()
            raise e


    def load_model(self, file_name):
        """
            Method Name: load_model
            Description: load the model file to memory
            Output: The Model file loaded in memory
            On Failure: Raise Exception
        """
        try:
            file = open('Logs/Model_operations_log.txt', 'a+')
            with open('models/' + file_name + '.pkl', 'rb') as f:
                self.logger.log(file, 'Model File ' + file_name + ' loaded')
                file.close()
                return pickle.load(f)

        except Exception as e:
            file = open('Logs/Model_operations_log.txt', 'a+')
            self.logger.log(file, f'Error occured : {e}')
            file.close()
            raise e

    def find_correct_model_for_cluster(self, cluster_number):
        """
            Method Name: find_correct_model_file
            Description: Select the correct model based on cluster number
            Output: The Model file
            On Failure: Raise Exception
        """
        try:
            file = open('Logs/Model_operations_log.txt', 'a+')
            self.cluster_number = cluster_number
            self.folder_name = 'models/'
            self.list_of_models = []
            self.list_of_files = os.listdir(self.folder_name)
            for model in self.list_of_files:
                try:
                    if (model.index(str( self.cluster_number))!=-1):
                        self.model_name=model

                except:
                    continue
            self.model_name = self.model_name.split('.')[0]
            self.logger.log(file,'Correct model loaded')
            return self.model_name

        except Exception as e:
            raise e










