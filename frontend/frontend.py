from backend.getData import * 
import matplotlib.pyplot as plt


country = input('Select a country: ')
city = input('If applicable, select a city: ')

province = input('If applicable, select a province: ')
status = input('Enter Status (confirmed, recovered, deaths): ')

data = getData.parseData(getData.getData(country,status), province, city)



x = data['days']
y = data['Totalcases']

plt.plot(x , y, 'o', color = 'black')
plt.ylabel('cases')
plt.xlabel('days')
plt.show()