import numpy as np
from collections import defaultdict
import random
import matplotlib.pyplot as plt

class K_Means_PlusPlus():
    ''' 
    Fits data into clusters using K-Means++. If data is 2-dimensional, plot_clusters plots a scatterplot of clusters after   
    model is fit. 
    '''
    
    def __init__(self, data):
        """
        input: 
            data:data: numpy array of data
        self.data: array of data 
        self.k: number of clusters desired
        self.centroids: list of centers, i.e. a list of lists
        self.assignment: dictionary, keys are ints, 0-k, values are arrays of data points in cluster 
                         coresponding to its key. The centroid associated with cluster with key i is
                         self.centroid[i].
        """
        self.data = data
        self.k = int
        self.centroids = list
        self.assignment = defaultdict()
    
    
    def initial_centers(self):
        """    
        initializes self.centroids    
        """  
        center0 = self.data[np.random.choice(len(self.data))]
        centers=[center0]
        for i in range(1,self.k): #1-k since we only need k-1 more centers
            distances_squared_to_centers=[]
            for center in centers:
                distances_squared_to_centers.append(((self.data-center)**2).sum(axis = 1))
            distance_squared_to_closest_center=np.array(distances_squared_to_centers).min(axis=0)
            prob_of_next_center= distance_squared_to_closest_center/distance_squared_to_closest_center.sum()
            center = self.data[random.choices(range(len(self.data)),weights=prob_of_next_center,k=1)]
            centers.append(center)
        self.centroids = np.array(centers)         
    
    
    def make_clusters(self):
        '''
        instanciates self.assignment if doesn't yet exist, else updates self.assignment based on self.centroids. 
        '''
        distances_to_centers = []
        for center in self.centroids:
            dist_to_center = (((self.data-center)**2).sum(axis = 1))**.5
            distances_to_centers.append(dist_to_center)
        closest = np.array(distances_to_centers).min(axis=0)
        in_cluster = (distances_to_centers == closest) #a boolean array with as many columns as data points,   
        clusters={}
        for i in range(self.k):
            cluster =[]
            for j in range(len(self.data)):
                if in_cluster[i][j] == True:
                    cluster.append(list(self.data[j]))
            clusters[i] = cluster
        self.assignment = clusters  

        
    def fit(self, k=3):
        """
        input: k (optional)
        output: none
        
        Takes in k and fits the model into k clusters until the clusters are not changed when refit. 
        """
        self.k = k
        keep_going = True
        self.initial_centers()
        self.make_clusters()
        while keep_going == True:
            new_centers= []
            init_clusters = self.assignment
            for i in range(self.k):
                new_centers.append(np.array(self.assignment[i]).mean(axis=0))
            self.centroids = np.array(new_centers)
            self.make_clusters()
            new_clusters = self.assignment
            still_clusters = 0
            for i in range(self.k):
                if init_clusters[i] == new_clusters[i]:
                    still_clusters+=1
            if still_clusters >= (self.k - 1):
                keep_going = False
              
            
    def get_assignments(self):
        """
        input: none
        output: self.assignment- dictionary with key = cluster number, value = list of points contained in it
        """
        return self.assignment

    
    def plot_clusters(self):
        """
        if data is 2-Dim, plots the data clusters
        """
        fig,ax =plt.subplots()
        for i in range(len(self.assignment)):
            x=[]
            y=[]
            for point in self.assignment[i]:
                x.append(point[0])
                y.append(point[1])
            ax.scatter(x,y)    
        
        