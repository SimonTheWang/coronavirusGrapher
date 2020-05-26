from datetime import datetime
import requests
import json

APIreference = ' refer to https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest for more info'
URL = "https://api.covid19api.com/"

def getCountries():
    allCountries = []
    response = requests.get(URL+'countries')
    data = response.json()
    for country in data:
        allCountries.append(country["Country"])
    return allCountries
def checkCountry(country):
    for place in requests.get(URL+'countries').json():
        for each in place.items():
            if country.lower() == place['Country'].lower() or country.lower() == place['Slug'].lower() or country == place['ISO2'].lower():
                return place['Slug']
    raise ValueError ('cannot find response, your value "' + country + '" is not a valid country' + APIreference)

def getData(country, status = 'confirmed'):
    countryInput = 'country/' + checkCountry(country)
    if status == '1' or status == 'confirmed' or status == '':
        status = 'confirmed'
    elif status == '2' or status == 'recovered':
        status = 'recovered'
    elif status == '3' or status == 'deaths':
        status = 'deaths'
    else:
        raise ValueError ('Value "'+ status + '" is invalid, please enter a number between 1 and 3')


    status = 'status/' + status.lower()
    parameters = {
    }

    response = requests.get(URL+'dayone'+'/'+countryInput+'/'+status+'/'+'live',parameters)
    
    data = response.json()

    return data
def searchProvinceCity(data):
    geoType = ''
    ProvinceCity = set()
    for datapoint in data:
        if datapoint['City']:
            ProvinceCity.add(datapoint['City'].lower())
            geoType = 'City'
        if datapoint['Province']:
            ProvinceCity.add(datapoint['Province'].lower())
            geoType = 'Province'
    data = {}
    data[geoType] = ProvinceCity
    return data

def parseData(data,geoType,provincecity = ''):
    days = []
    dates = []
    totalCases = []
    casesPerDay = []
    info = {}
    count = 0
    info['country'] = data[0]['Country'].capitalize()
    info['provincecity'] = provincecity.capitalize()
    for subject in range(len(data)):
        if ((list(geoType.keys()))[0]):
            if provincecity.lower() in geoType['Province'] or provincecity.lower() in geoType['City']:
                if provincecity.lower() == (data[subject])[(''.join(list(geoType.keys())))].lower():
                    totalCases.append(data[subject]['Cases'])
                    count+=1
                    days.append(count)
                    dates.append(data[subject]['Date'])
            else:
                raise ValueError ( 'Your input of either city or province is invalid, the database does not contain "'+ provincecity + '" for ' + info['country'] + APIreference)
        else:
            totalCases.append(data[subject]['Cases'])
            count+=1
            days.append(count)
            dates.append(data[subject]['Date'])
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
