import pandas
import os
import shutil
from File_Operation.model_methods import model_operations
from Data_Preprocessing.preprocessing import Preprocessor
from Data_Loader.loader_prediction import Data_loader_Pred
from Logger.Logger import Applogger
from Prediction_Raw_Data_Validation.prediction_raw_validation import PredDatavalidation

class model_prediction:


    def __init__(self,path):
        self.logger = Applogger()
        self.pred_data_val = PredDatavalidation(path)


    def prediction_from_model(self):

        try:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            self.pred_data_val.deletePredictionFile() #deletes the existing prediction file from last run!
            data_getter = Data_loader_Pred()
            df = data_getter.get_data()
            self.logger.log(file, 'Data loaded successfully')

            self.logger.log(file, 'Preprocessing started !!')
            preprocessor = Preprocessor()
            is_null_present = preprocessor.is_null_present(df)
            print(is_null_present)

            if (is_null_present):
                df = preprocessor.impute_missing_values(df)
            self.logger.log(file, 'Missing values imputed !!')
            cols_to_drop = preprocessor.get_columns_with_zero_std_deviation(df)
            df = preprocessor.remove_col(df, cols_to_drop)
            self.logger.log(file, 'Column removed !!')
            self.logger.log(file, 'Preprocessing ended!!')

            # no error up to preprocessing

            file_loader = model_operations()
            kmeans = file_loader.load_model('KMeans')

            self.logger.log(file, 'KMeans file loaded')



            clusters = kmeans.predict(df)  #  cluster prediction
            print(clusters)
            df['clusters'] = clusters
            list_of_clusters = list(df['clusters'].unique())

            self.logger.log(file, 'Clusters created')

            count = 0
            if os.path.isdir('prediction_output_files'):
                shutil.rmtree('prediction_output_files')
            os.mkdir('prediction_output_files')

            for cluster in list_of_clusters:
                cluster_data = df[df['clusters'] == cluster]

                cluster_data = cluster_data.drop(['clusters'], axis=1)

                model_name = file_loader.find_correct_model_for_cluster(cluster)

                model = file_loader.load_model(model_name)
                self.logger.log(file, 'Correct model loaded')

                result = list(model.predict(cluster_data))

                result = pandas.DataFrame(list(zip(result)), columns=['Prediction'])
                self.logger.log(file, 'Result exported in dataframe')
                print(result)

                path = "prediction_output_files/Predictions.csv"

                result.to_csv(path, header=True, mode='a+')  # appends result to prediction file

            self.logger.log(file, 'End of Prediction')

            file.close()
            return path, result.head().to_json(orient="records")

        except Exception as e:
            file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
            self.logger.log(file, f'Error : {e}')
            raise e








