from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, accuracy_score
from Logger.Logger import Applogger

class ModelFinder:

    def __init__(self):
        self.logger = Applogger()
        self.RF_clf = RandomForestClassifier()
        self.xgb = XGBClassifier(objective='binary:logistic')
        self.svm = SVC()

    def get_best_params_for_rf(self, train_x, train_y):
        """
            Method Name: get_best_params_for_random_forest
            Description: get the parameters for Random Forest Algorithm which give the best accuracy.
                         Use Hyper Parameter Tuning.
            Output: The model with the best parameters
            On Failure: Raise Exception
        """
        try :
            # initisalizing with a diff combination of parameters
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            self.param_grid = {
                               "n_estimators": [10, 50, 100],
                               "criterion": ['gini', 'entropy'],
                               "max_depth": range(2,4),
                               }

            # creating object of grid search class
            self.grid = GridSearchCV(estimator=self.RF_clf, param_grid=self.param_grid, cv=5, verbose=3)

            # finding the best parameters
            self.grid.fit(train_x, train_y)
            self.logger.log(file, f'RF best params : {str(self.grid.best_params_)}')

            # extracting the best parameters

            self.criterion = self.grid.best_params_['criterion']
            self.max_depth = self.grid.best_params_['max_depth']
            self.n_estimators = self.grid.best_params_['n_estimators']


            # creating a new model with the best parameters
            self.RF_clf = RandomForestClassifier(n_estimators=self.n_estimators, criterion=self.criterion,
                                              max_depth=self.max_depth)
            self.logger.log(file,'model crated with best fitted parameters')

            # training the mew model
            self.RF_clf.fit(train_x, train_y)
            self.logger.log(file, 'RF model trained')

            file.close()
            return self.RF_clf

        except Exception as e:
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            self.logger.log(file, f'Error occured : {e}')
            raise e



    def get_best_param_for_svc(self, train_x, train_y):

        try :
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            param_grid={
                        'gamma':['scale', 'auto',.001,.02,.1]
                        }
            self.grid = GridSearchCV(estimator=self.svm, param_grid=param_grid, cv=5, verbose=3)

            # extracting the best parameters
            self.grid.fit(train_x, train_y)
            self.logger.log(file, f'SVC best params : {str(self.grid.best_params_)}')

            # extracting the best parameters
            self.gamma= self.grid.best_params_['gamma']

            # creating a new model with the best parameters
            self.svm = SVC(gamma=self.gamma, decision_function_shape='ovo')
            self.logger.log(file, 'model crated with best fitted parameters')


            # training the mew model
            self.svm.fit(train_x, train_y)
            self.logger.log(file, 'SVM model trained')

            file.close()
            return self.svm


        except Exception as e:
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            self.logger.log(file, f'Error Occured : {e}')
            raise e



    def get_best_model(self, train_x, train_y, test_x, test_y):
        """
            Method Name: get_best_model
            Description: Find out the Model which has the best AUC score.
            Output: The best model name and the model object
            On Failure: Raise Exception
        """

        try:
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            # CREATE BEST MODEL FOR SVM
            self.svc = self.get_best_param_for_svc(train_x, train_y)

            self.prediction_svc = self.svm.predict(test_x)

            if len(test_y.unique()) == 1: # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.svc_score = accuracy_score(test_y, self.prediction_svc)
                self.logger.log(file, 'Accuracy for RF:' + str(self.svc_score))
            else:
                self.svc_score = roc_auc_score(test_y, self.prediction_svc)
                self.logger.log(file, 'AUC for RF:' + str(self.svc_score))


            # CREATE BEST MODEL FOR RANDOM FOREST
            self.random_forest = self.get_best_params_for_rf(train_x, train_y)

            self.prediction_random_forest = self.random_forest.predict(test_x)

            if len(test_y.unique()) == 1:  # if there is only one label in y, then roc_auc_score returns error. We will use accuracy in that case
                self.random_forest_score = accuracy_score(test_y, self.prediction_random_forest)
                self.logger.log(file, 'Accuracy for RF:' + str(self.random_forest_score))

            else:
                self.random_forest_score = roc_auc_score(test_y, self.prediction_random_forest)  # AUC for Random Forest
                self.logger.log(file, 'AUC for RF:' + str(self.random_forest_score))


            # COMPARING TWO MODELS

            if (self.random_forest_score < self.svc_score):
                self.logger.log(file, 'Best model SVM returned')
                file.close()
                return 'SVM', self.svc
            else:
                self.logger.log(file, 'Best model Random Forest returned')
                file.close()
                return 'RandomForest', self.random_forest

        except Exception as e:
            file = open('Logs/Training_Logs/parameter_tuner_log.txt', 'a+')
            self.logger.log(file, f'Error Occured : {e}')
            file.close()
            raise e







