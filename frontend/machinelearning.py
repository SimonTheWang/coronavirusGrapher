from getData import *
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics

LIMIT = 1000
def machineLearning(data):
    print('request received')
    x = data['days'].copy()
    y1 = data['totalCases'].copy()
    y2 = data['casesPerDay'].copy()

    x_new = np.array(x) # Transforms list into an array
    y2_new = np.array(y2)

    x_new2 = x_new.reshape(-1, 1) # Transforms 1d array into a 2d array
    y2_new = y2_new.reshape(-1, 1)



    poly_reg = PolynomialFeatures(degree = 2) # Degree 2 polynomial is a parabola. We have tried using different degrees, but higher degrees usually makes the function vary a lot more, thus being more inacurate
    x_poly = poly_reg.fit_transform(x_new2) # Most commands related to polynomial regression were taken from here: https://towardsdatascience.com/a-beginners-guide-to-linear-regression-in-python-with-scikit-learn-83a8f7ae2b4f
    pol_reg = LinearRegression() # Adopted the commands for my use
    pol_reg.fit(x_poly, y2_new)


    future_x = [] # List for future dates
    predicted_y_perDay = [] # Predicted new cases per day
    predicted_y_total =[] # Predicted total cases

    # Machine learning part
    i = 1  
    while i<=LIMIT: 
        i+=1
        random_list = [ x[len(x) - 1] + i ]
        random_array = np.array(random_list)
        random_array_reshaped = random_array.reshape(-1, 1)
        random_predicted_y_value = pol_reg.predict(poly_reg.fit_transform(random_array_reshaped))
        # Usually people train the data set before making a fit and predicting future data points, but since we didn't have a lot of data to begin with, we just used all the data
        if random_predicted_y_value >= 1:
            future_x.append(x[len(x) - 1] + i)
            predicted_y_perDay.append(int(random_predicted_y_value))

        else:
            break
    data['i'] = i
    if i> LIMIT:# possibility of a positive equation, which would be infinite
        print('unable to predict cases reliably')

    firstDay = data['totalCases'][-1]
    perDay1 = predicted_y_perDay.copy() # computes cases per day using total cases 
    perDay2 = []

    for cases in range(len(perDay1)): # computes total cases per day
        if cases == 0:
            perDay2.append(firstDay + perDay1[cases])
        else:
            perDay2.append(perDay1[cases] + perDay2[cases-1])



    daysPredicted = []
    totalPredicted = []
    perDayPredicted = []
    

    daysPredicted = future_x
    totalPredicted = perDay2
    perDayPredicted = predicted_y_perDay


    data['daysPredicted'] = daysPredicted # gives computed data and returns it
    data['totalPredicted'] = totalPredicted
    data['perDayPredicted'] = perDayPredicted
    
    return data


