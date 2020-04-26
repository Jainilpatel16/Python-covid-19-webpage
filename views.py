from django.shortcuts import render
import base64
import io
import urllib
from datetime import datetime
import requests

import matplotlib.pyplot as plt
from django.http import HttpResponse

def homepage(request):
    now = datetime.now()
    return HttpResponse("Welocome to the homepage. The time is: %s" %now)

def covid19page(request):
    dates = [
        '2020-03-15', '2020-03-16', '2020-03-17', '2020-03-20', '2020-04-01', '2020-04-10', '2020-04-12', '2020-04-17'
    ]
    italydata = []
    gdata = []

    # get data from API
    for d in dates:
        response = requests.get(
            'https://api.covid19api.com/country/italy/status/confirmed?from=%sT00:00:00Z&to=2020-04-18' %d)
        Data = response.json()
        Result = Data[0]
        italydata.append(Result['Cases'])


    for d in dates:
        gresponse = requests.get(
            'https://api.covid19api.com/country/germany/status/confirmed?from=%sT00:00:00Z&to=2020-04-18' %d)
        gData = gresponse.json()
        gResult = gData[0]
        gdata.append(gResult['Cases'])


    # plot the data
    plt.title("Covid-19 cases in GREMANY and ITALY")
    plt.plot(dates, italydata)
    plt.plot(dates, gdata)
    plt.xlabel('Date')
    plt.ylabel('Number of Cases')
    plt.ylim((3000, 180000))
    plt.legend(["Italy", "Germany"])
    plt.grid()
    plt.gcf().autofmt_xdate()
    # generate figure and send it to the html template

    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return render(request, 'home.html', {'data': uri})

# Create your views here.
