from datetime import datetime
import requests
import json

APIreference = ' refer to https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest for more info'
URL = "https://api.covid19api.com/"

def getCountries():
    response = requests.get(URL+'countries')
    data = response.json()
    return data

def displayCountries(data):
    allCountries = []
    for country in data:
        allCountries.append(country["Country"])
        data = ', '.join(allCountries)
    return data
    
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
    if data:
        return data
    else:
        raise ValueError ('Data for ' + country +' parsed as ' + countryInput +' is not found')

def searchProvince(data):# dictionary with keys '' or province names
    geoType = ''
    place = {}
    place[''] = set()
    for datapoint in data:
        if datapoint['Province'] and datapoint['Province'] not in place.keys():
            place[datapoint['Province']] = set()

        if datapoint['City']:
            if place[datapoint['Province']]:
                place[datapoint['Province']].add(datapoint['City'])
            else:
                place[''].add(datapoint['City'])
    return place

def parseData(data,geoType,province='', city = ''):
    days = []
    dates = []
    totalCases = []
    casesPerDay = []
    info = {}
    count = 0
    info['country'] = data[0]['Country'].capitalize()
    info['province'] = province.capitalize()
    info['city'] = city.capitalize()
    for subject in data:
        if (((province and city and province.title() == subject['Province'].title() and city.title() == subject['City'].title())) or ((province and not city) and (province.title() == subject['Province'].title())) or ((not province and city and city.title() == subject['City'].title())) or (not province and not city)):
            totalCases.append(subject['Cases'])
            count+=1
            days.append(count)
            dates.append(subject['Date'])
        
    if count ==0:
        raise ValueError ( 'Your input of either city or province is invalid, the database does not contain "'+ province+ city + '" for ' + info['country'] + APIreference)
    info['totalCases'] = totalCases
    info['days'] = days
    info['dates'] = dates
    info['type'] = subject['Status']
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


