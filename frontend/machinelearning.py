from getData import *
from frontend import *
import pandas as pd  
import numpy as np  
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn import metrics


#print(type(x))

x_new = np.array(x)
y2_new = np.array(y2)

x_new2 = x_new.reshape(-1, 1)
y2_new2 = y2_new.reshape(-1, 1)

"""
model = LinearRegression()
model.fit(x_new2, y2_new2)
print(model.intercept_) #intercept
print(model.coef_)      #slope

y_pred = model.predict(x_new2)
df = pd.DataFrame({'Actual': y2_new2.flatten(), 'Predicted': y_pred.flatten()})
print(df)

plt.scatter(x, y2,  color='gray')
plt.plot(x, y_pred, color='red', linewidth=2)
plt.show()

#print(len(x))
#print(y1)
"""

poly_reg = PolynomialFeatures(degree = 2)
x_poly = poly_reg.fit_transform(x_new2)
pol_reg = LinearRegression()
pol_reg.fit(x_poly, y2_new2)


future_x_dates = []
predicted_y_list = []

for i in range(1, 100):
    random_list = [ x[len(x) - 1] + i ]
    random_array = np.array(random_list)
    random_array_reshaped = random_array.reshape(-1, 1)
    random_predicted_y_value = pol_reg.predict(poly_reg.fit_transform(random_array_reshaped))
    if random_predicted_y_value >= 0:
        future_x_dates.append(x[len(x) - 1] + i)
        predicted_y_list.append(int(random_predicted_y_value))
    else:
        break

print(future_x_dates)
print(predicted_y_list)



plt.scatter(x, y2, color='red')
plt.scatter(future_x_dates, predicted_y_list, color='green')
plt.plot(x_new2, pol_reg.predict(poly_reg.fit_transform(x_new2)), color='blue')
plt.title('Coronavirus prediction (Polynomial Regression degree 2)')
plt.xlabel('Number of days')
plt.ylabel('Number of new cases')
plt.show()