# from ..backend import getData
from getData import *

import matplotlib.pyplot as plt


country = input('Select a country: ')
city = input('If applicable, select a city: ')

province = input('If applicable, select a province: ')
status = input('Enter Status number (1 : (confirmed) , 2 : (recovered) , 3 : (deaths): ')

data = parseData(getData(country,status), province, city)


#sets the data
x = data['days']
y1 = data['totalCases']
y2 = data['casesPerDay']
y11 = [1,2,3,4,5]
y22 = [1,2,3,4,5]
# plot the data
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(x, y1, '-' , color='tab:blue', label = 'total cases')
ax.plot(x, y2,'-', color='tab:orange', label = 'cases per day')
ax.plot(x, y2,'--', color='tab:blue', label = 'predicted total cases')
ax.plot(x, y2,'--', color='tab:orange', label = 'predicted cases per day')

ax.set_xlabel('number of days')
ax.set_ylabel(('cases of status : ' + data['type']))
ax.legend()
ax.set_title('# of cases of status: ' + data['type'] + ', with respect to time, starting from ' + data['day1'])

# display the plot
plt.show()