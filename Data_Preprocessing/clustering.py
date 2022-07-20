import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_Operation.model_methods import model_operations
from Logger.Logger import Applogger
import os

class KMeanClustering:
    """
        This class shall be use for dividing the dataset into clusters before training
    """

    def __init__(self):
        self.logger = Applogger()

    def elbow_plot(self, df):
        """
            Method Name: elbow_plot
            Description: This method saves the plot to decide the optimum number of clusters to the file.
            Output: A picture saved to the directory
            On Failure: Raise Exception
        """
        self.df = df
        try:
            file = open('Logs/clustering.txt', 'a+')
            if not os.path.isdir('ClusteringGraph/'):
                os.makedirs('ClusteringGraph/')
            wcss = []
            for i in range(1,11):
                kmeans = KMeans(n_clusters=i, init= 'k-means++', random_state=42)   # initializing the kmeans object
                kmeans.fit(self.df)   #fitting the data
                wcss.append(kmeans.inertia_)

            # PLOTTING THE ELBOW PLOT
            plt.plot(range(1, 11), wcss)  # creating the graph between WCSS and the number of clusters
            plt.title('The Elbow Method')
            plt.xlabel('Number of clusters')
            plt.ylabel('WCSS')
            plt.savefig('ClusteringGraph/K-Means_Elbow.png')  # saving the elbow plot locally

            self.logger.log(file, 'Elbow plot created and saved successfully ')

            # FINDING THE VALUE OF OPTIMUM NUMBER OF CLUSTER
            self.kn = KneeLocator(range(1,11), wcss, curve='convex', direction='decreasing')
            self.logger.log(file, 'The optimum number of clusters is: ' + str(self.kn.knee) )
            file.close()
            return self.kn.knee

        except Exception as e :
            raise e


    def create_cluster(self, df, number_of_cluster):
        """
        Method Name: create_clusters
        Description: Create a new dataframe consisting of the cluster information.
        Output: A datframe with cluster column
        On Failure: Raise Exception

        """
        self.df = df
        self.number_of_cluster = number_of_cluster
        try:
            file = open('Logs/clustering.txt', 'a+')

            self.kmeans = KMeans(n_clusters= self.number_of_cluster, init='k-means++', random_state= 42)
            self.y_kmeans = self.kmeans.fit_predict(self.df)     # divide the dataset into clusters.
            self.logger.log(file, 'successfully created ' + str(self.kn.knee) + 'clusters')

            self.file_op = model_operations()
            self.file_op.save_model(self.kmeans, 'KMeans')   # saving the KMeans model to directory
            self.logger.log(file, 'KMeans model saved successfully!!!')

            self.df['Cluster'] = self.y_kmeans    # create a new column in dataset for storing the cluster information

            self.logger.log(file, 'succesfully created ' + str(self.kn.knee) + 'clusters')
            file.close()
            return self.df

        except Exception as e:
            file = open('Logs/clustering.txt', 'a+')
            self.logger.log(file, 'KMeans model saved successfully!!!')
            file.close()
            raise e








