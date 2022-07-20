import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from flask_cors import CORS
import flask_monitoringdashboard as dashboard
from flask_cors import cross_origin
from Logger.Logger import Applogger
from File_Operation.model_methods import model_operations

app = Flask(__name__)
dashboard.bind(app)
CORS(app)


@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict", methods=['POST'])
@cross_origin()
def predict():
    logger = Applogger()
    file = open('Logs/Prediction_Logs/prediction_log.txt', 'a+')
    '''
        for rendering results on HTML
        '''
    features = [int(x) for x in request.form.values()]
    logger.log(file, 'information collected from web ui')

    # re-arranging the list as per data set
    feature_list = [features[4]] + features[:4] + features[5:11][::-1] + features[11:17][::-1] + features[17:][::-1]
    features_arr = [np.array(feature_list)]

    # converting the array into a pandas dataframe
    col_names = ["LIMIT_BAL", "SEX","EDUCATION", "MARRIAGE", "AGE","PAY_0","PAY_2","PAY_3",
                                               "PAY_4", "PAY_5","PAY_6","BILL_AMT1","BILL_AMT2", "BILL_AMT3","BILL_AMT4","BILL_AMT5", "BILL_AMT6",
                                               "PAY_AMT1","PAY_AMT2","PAY_AMT3","PAY_AMT4","PAY_AMT5","PAY_AMT6"]
    df = pd.DataFrame(features_arr, columns= col_names)

    # predicting the cluster for the dataset
    file_loader = model_operations()
    kmeans = file_loader.load_model('KMeans')
    cluster = kmeans.predict(df)  # cluster prediction
    logger.log(file, f'possible cluster predicted. cluster : {cluster[0]}th')

    # finding the correct model for the predicted cluster
    model_name = file_loader.find_correct_model_for_cluster(cluster[0])
    logger.log(file, f'model for cluster {cluster[0]} is {model_name}')

    # loading the model
    model = file_loader.load_model(model_name)
    logger.log(file, 'Model loaded !!!')

    # doing the prediction
    prediction = model.predict(features_arr)
    logger.log(file, 'Prediction complete, returning the value!!')

    result = ""
    if prediction == 1:
        result = "The credit card holder WILL BE DEFAULTER in the next month"
    else:
        result = "The Credit card holder WILL NOT BE DEFAULTER in the next month"

    logger.log(file, 'Result returned !!')

    return render_template('index.html', prediction_text=result)

if __name__=='__main__':
    app.run()