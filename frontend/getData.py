from datetime import datetime
import requests
import json

APIreference = ' refer to https://documenter.getpostman.com/view/10808728/SzS8rjbc?version=latest for more info'
URL = "https://api.covid19api.com/"

def getCountries():
    ''' searches covid19api for available countries in their database '''
    response = requests.get(URL+'countries')
    data = response.json()
    return data

def displayCountries(data):
    ''' returns countries from getCountries as a list '''
    allCountries = []
    for country in data:
        allCountries.append(country["Country"])
        data = ', '.join(allCountries)
    return data
    
def checkCountry(country):
    ''' Checks for validity of inputted Country, 
    note that some countries marked as 'available' may return an error 
    because the api does not currently have information on them.
    This function also returns the slug of a given country to make its request to the api easier'''
    for place in requests.get(URL+'countries').json():
        for each in place.items():
            if country.lower() == place['Country'].lower() or country.lower() == place['Slug'].lower() or country == place['ISO2'].lower():
                return place['Slug']
    raise ValueError ('cannot find response, your value "' + country + '" is not a valid country' + APIreference)

def getData(country, status = 'confirmed'):
    ''' makes a request to the api, using user inputs and checkCountry slug.
    returns a dictionary containing all the information from that area from day one of the outbreak there'''
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
    ''' Using data in getData(), returns a dictionary containing 
    key-value pairs of Provinces and their cities, which are a set, for a country.
    If not present, the province will be replaced by ''  '''
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

def parseData(data,province='', city = ''):
    ''' Using data from getData() and user data, this returns a dictionary containing
    data on the given area, including the number of cases per day and the total cases per day, 
    and returns an error if the province or city do not match with the country.'''
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
        #appends data only for corresponding province-city
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




    previousTotalCases = totalCases.copy()# computes cases per day using total cases 
    previousTotalCases.insert(0,0)
    afterTotalCases = totalCases.copy()
    afterTotalCases.append(0)
    for day1,day2 in zip(previousTotalCases,afterTotalCases):
        casesPerDay.append(day2-day1)
    casesPerDay.pop()
    info['casesPerDay'] = casesPerDay 

    return info


