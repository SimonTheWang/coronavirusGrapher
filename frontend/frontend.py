# from ..backend import getData
from getData import *

import matplotlib.pyplot as plt

print('available countries are: ' + ', '.join(getCountries()) )
country = input('Select a country: ')
status = input('Enter Status number (1 : (confirmed) , 2 : (recovered) , 3 : (deaths): ')
possibleProvinceCity = (searchProvinceCity(getData(country,status)))
procity = (', '.join(list(possibleProvinceCity.keys())))
print('available '+ procity + 's are ' + (', '.join(list(possibleProvinceCity[procity]))))
provincecity = input('If applicable, select a city or province: ')



data = parseData(getData(country,status),(possibleProvinceCity),provincecity)
print
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
ax.set_title('# of cases of status: ' + data['type'] + ', with respect to time, starting from ' + data['day1'] +' in '+ data['provincecity'] + ', ' + data['country'])

# display the plot
plt.show()