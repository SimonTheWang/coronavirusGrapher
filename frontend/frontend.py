# from ..backend import getData
from getData import *

import matplotlib.pyplot as plt

print('available countries are: ' + displayCountries(getCountries()) )

country = (input('Select a country: '))
status = input('Enter Status number (1 : (confirmed) , 2 : (recovered) , 3 : (deaths): ')

possibleProvinceCity = (searchProvince(getData(country)))
 
possibleProvinces = ', '.join(list(possibleProvinceCity.keys()))
if possibleProvinces:
    print('Available provinces are: ' + possibleProvinces)
    province = (input('Enter a province: ').title())
    possibleCities = ', '.join(list(possibleProvinceCity[province]))
    if possibleCities:
        print('Available cities are: ' + possibleCities)
        city = input('Enter a City')
    else:
        city = ''
elif possibleProvinceCity['']:
    possibleCities = ', '.join(list(possibleProvinceCity[''].values()))
    print('Available cities are: ' + possibleCities)
    city = input('Enter a City') 
else:
    province = ''
    city = ''

if province:
    if city:
        print('Province: ' + provincexuadore + ' City: ' + city)
    elif not city:
        print('Processing input of : Country: ' +  country  + 'Province: ' + province + ' City: ' + city)
else:
    print('Processing input of: ' +country)


data = parseData(getData(country,status),(possibleProvinceCity),province, city)
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
ax.set_title('# of cases of status: ' + data['type'] + ', with respect to time, starting from ' + data['day1'] +' in '+ data['province'] + data['city'] + ', ' + data['country'])

# display the plot
plt.show()