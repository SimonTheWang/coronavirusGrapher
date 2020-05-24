import sys
sys.path.append('C:/Users/foubroker/Desktop/FinalProject/coronavirusGrapher/backend/')
import getData

country = input('Select a country: ')
city = input('If applicable, select a city: ')

province = input('If applicable, select a province: ')
status = input('Enter Status (confirmed, recovered, deaths): ')

data = getData.parseData(getData.getData(country,status), province, city)

import matplotlib.pyplot as plt


x = data['days']
y = data['Totalcases']

plt.plot(x , y, 'o', color = 'black')
plt.ylabel('cases')
plt.xlabel('days')
plt.show()
#gfhgfjg
