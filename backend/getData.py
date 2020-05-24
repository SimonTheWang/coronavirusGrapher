from datetime import datetime
import requests
import json

def getData(country, status = 'confirmed', fromUTC = "2020-03-01T00:00:00Z", toUTC = datetime.utcnow()):
    country = 'country/' + country.lower();
    status = '/status/' + status.lower()
    parameters = {
        "from" : fromUTC,
        "to" : toUTC,
    }

    response = requests.get("https://api.covid19api.com/"+country+status,parameters)
    data = response.json()
    return data

def parseData(data,province = '',city= ''):
    days = []
    dates = []
    cases = []
    info = {}
    count = 0
    for day in range(len(data)):
        if (province.lower() == (data[day])['Province'].lower() or not province) and (city == (data[day])['City'].lower() or not city.lower()):
            cases.append(data[day]['Cases'])
            count+=1
            days.append(count)
            dates.append(data[day]['Date'])
    info['Totalcases'] = cases
    info['days'] = days
    info['dates'] = dates
    print(info)
    return info
