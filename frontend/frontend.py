# from ..backend import getData
from getData import *
from scipy import stats

import matplotlib.pyplot as plt

print('available countries are: ' + displayCountries(getCountries()) )
country = (input('Select a country: '))
status = input('Enter Status number (1 : (confirmed) , 2 : (recovered) , 3 : (deaths): ')

possibleProvinceCity = (searchProvince(getData(country)))# searches for possible provinces and/or cities tied to the country

possibleProvinces = ', '.join(list(possibleProvinceCity.keys()))

if possibleProvinces:# makes additional inputs for province and/or cities if needed
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

if province:# confirms input
    if city:
        print('Processing input of : Country: ' +  country  + ', Province: ' + province + ', City: ' + city)
    elif not city:
        print('Processing input of : Country: ' +  country  + ', Province: ' + province )
else:
    print('Processing input of: ' +country)


#sets the data
data = parseData(getData(country,status),(possibleProvinceCity),province, city)
print(data)

x = data['days']
y1 = data['totalCases']
y2 = data['casesPerDay']
y11 = ['']
y22 = ['']
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