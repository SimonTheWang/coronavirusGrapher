# from ..backend import getData
from getData import *
from machinelearning import *

import numpy as np
import matplotlib.pyplot as plt

LIMIT = 1000
def run():
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
    data = machineLearning(parseData(getData(country,status),province, city))
    if data['daysPredicted']and data['type'] == 'confirmed':
        if data['i']  != LIMIT:
            print('expected resolution on day '+ str(data['daysPredicted'][-1]))

    x1 = (data['days'])
    x2 = data['daysPredicted']
    y1 = (data['totalCases'])
    y2 = (data['casesPerDay'])
    y11 = (data['perDayPredicted'])
    y22 = (data['totalPredicted'])

    # plot the data
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    if data['i'] != LIMIT:
        ax.plot(x2, y22,'--', color='tab:blue', label = 'predicted total cases')
        ax.plot(x2, y11,'--', color='tab:orange', label = 'predicted cases per day')
    plt.scatter(x1, y1,s= 1, color='tab:blue', label = 'total cases')
    plt.scatter(x1, y2,s = 1, color='tab:orange', label = 'cases per day')


    ax.set_xlabel('number of days')
    ax.set_ylabel(('cases of status : ' + data['type']))
    ax.legend()
    ax.set_title('# of cases of status: ' + data['type'] + ', with respect to time, starting from ' + data['day1'] +' in '+ data['province'] + data['city'] + ', ' + data['country'])

    # display the plot
    return plt.show()
