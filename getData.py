import requests
import json

def getData(country, status, fromUTC, toUTC):
    country = 'country/' + country;
    status = '/status/' + status
    parameters = {
        "from" : fromUTC,
        "to" : toUTC,
    }

    response = requests.get("https://api.covid19api.com/"+country+status,parameters)
    data = response.json()
    return data

def parseData(data,province = '',city= ''):
    days = []
    cases = []
    count = 0
    for day in range(len(data)):
        if (province == data[day]['Province'] or not province) and (city == data[day]['City'] or not city):
            cases.append(data[day]['Cases'])
            count+=1
            days.append(count)
    print(cases)
    print(days)
    return








x = getData("Canada", "confirmed", "2020-03-01T00:00:00Z", "2020-04-24T00:00:00Z")
parseData(x, 'Quebec')