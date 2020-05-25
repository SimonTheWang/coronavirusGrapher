from datetime import datetime
import pytz
import requests
import json

APIreference = ' refer to https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest for more info'

def getData(country, status = 'confirmed', fromUTC = "2020-03-01T00:00:00Z", toUTC = datetime.utcnow()):
    countryInput = 'country/' + country.lower();
    if status == '1':
        status = 'confirmed'
    elif status == '2':
        status = 'recovered'
    elif status == '3':
        status = 'confirmed'
    else:
        raise ValueError ('Value "'+ status + '" is invalid, please enter a number between 1 and 3')


    status = '/status/' + status.lower()
    parameters = {
        "from" : fromUTC,
        "to" : toUTC,
    }

    response = requests.get("https://api.covid19api.com/"+countryInput+status,parameters)
    
    data = response.json()
    if type(data) == str:
        raise ValueError ('cannot find response, your value "' + country + '" is not a valid country' + APIreference)
    return data

def parseData(data,province = '',city= ''):
    days = []
    dates = []
    totalCases = []
    casesPerDay = []
    info = {}
    count = 0
    info['country'] = data[0]['Country']
    for subject in range(len(data)):
        if (province.lower() == (data[subject])['Province'].lower()) and (city == (data[subject])['City'].lower()):
            totalCases.append(data[subject]['Cases'])
            count+=1
            days.append(count)
            dates.append(data[subject]['Date'])
        if count == 0:
            raise ValueError ( 'Your input of city or province is invalid, the database does not contain "'+ city + province + ' for ' + info['country'] + APIreference)
    info['totalCases'] = totalCases
    info['days'] = days
    info['dates'] = dates
    info['type'] = (data[subject])['Status']
    info['day1'] = ''.join((data[0])['Date'].split())[:-10]



    previousTotalCases = totalCases.copy()
    previousTotalCases.insert(0,0)
    afterTotalCases = totalCases.copy()
    afterTotalCases.append(0)
    for day1,day2 in zip(previousTotalCases,afterTotalCases):
        casesPerDay.append(day2-day1)
    casesPerDay.pop()
    info['casesPerDay'] = casesPerDay 

    return info
