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

    x_new = np.array(x)
    y2_new = np.array(y2)

    x_new2 = x_new.reshape(-1, 1)# forms list into 2d
    y2_new = y2_new.reshape(-1, 1)



    poly_reg = PolynomialFeatures(degree = 2) # parabola
    x_poly = poly_reg.fit_transform(x_new2)
    pol_reg = LinearRegression()
    pol_reg.fit(x_poly, y2_new)


    future_x = []
    predicted_y_perDay = []
    predicted_y_total =[]

    i=1 # machine learning 
    while i<=LIMIT:
        i+=1
        random_list = [ x[len(x) - 1] + i ]
        random_array = np.array(random_list)
        random_array_reshaped = random_array.reshape(-1, 1)
        random_predicted_y_value = pol_reg.predict(poly_reg.fit_transform(random_array_reshaped))
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


